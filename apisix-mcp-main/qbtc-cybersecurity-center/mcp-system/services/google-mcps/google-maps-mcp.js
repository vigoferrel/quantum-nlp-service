const { Client } = require('@googlemaps/google-maps-services-js');
const { MCPServer } = require('./mcp-server');

// Performance optimizations
const CACHE_TTL = 3600; // 1 hour for geocoding results
const MAX_BATCH_SIZE = 50;
const DEFAULT_SEARCH_RADIUS = 5000; // 5km
const geocodeCache = new Map();
const placesCache = new Map();
const pendingBatches = new Map();

// Initialize Maps client with optimized settings
const client = new Client({
    config: {
        timeout: 10000, // 10 seconds timeout
        retryOptions: {
            maxRetries: 3,
            maxRetryDelay: 2000,
            retryableErrorCodes: ['ECONNRESET', 'ETIMEDOUT', 'ECONNABORTED']
        },
        axiosOptions: {
            maxContentLength: 10 * 1024 * 1024, // 10MB
            maxBodyLength: 10 * 1024 * 1024 // 10MB
        }
    }
});

// Cache management
const getFromCache = (cache, key) => {
    const cached = cache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL * 1000) {
        return cached.data;
    }
    return null;
};

const addToCache = (cache, key, data) => {
    cache.set(key, {
        data,
        timestamp: Date.now()
    });
};

// Batch processing
const addToBatch = (batchKey, item) => {
    if (!pendingBatches.has(batchKey)) {
        pendingBatches.set(batchKey, []);
    }
    pendingBatches.get(batchKey).push(item);

    if (pendingBatches.get(batchKey).length >= MAX_BATCH_SIZE) {
        return processBatch(batchKey);
    }
    return null;
};

const processBatch = async (batchKey) => {
    const items = pendingBatches.get(batchKey);
    pendingBatches.delete(batchKey);
    return items;
};

// Error handling wrapper
const withErrorHandling = async (operation) => {
    try {
        return await operation();
    } catch (error) {
        console.error(`Operation failed: ${error.message}`);
        if (error.response?.data?.error_message) {
            throw new Error(error.response.data.error_message);
        }
        throw error;
    }
};

// Utility functions
const validateLatLng = ({ lat, lng }) => {
    return typeof lat === 'number' && 
           typeof lng === 'number' && 
           lat >= -90 && lat <= 90 && 
           lng >= -180 && lng <= 180;
};

const formatPlaceResult = (place) => {
    return {
        id: place.place_id,
        name: place.name,
        address: place.formatted_address,
        location: place.geometry?.location,
        rating: place.rating,
        types: place.types,
        openNow: place.opening_hours?.open_now,
        photos: place.photos?.map(photo => ({
            reference: photo.photo_reference,
            width: photo.width,
            height: photo.height
        }))
    };
};

// Create MCP Server with optimizations
const startServer = async () => {
    const server = new MCPServer();

    // Geocoding operations
    server.on('geocode', async (params) => {
        const { address, batch = false } = params;
        const cacheKey = `geocode:${address}`;

        return withErrorHandling(async () => {
            // Check cache first
            const cached = getFromCache(geocodeCache, cacheKey);
            if (cached) return cached;

            // Handle batch requests
            if (batch) {
                return addToBatch('geocoding', { address });
            }

            const response = await client.geocode({
                params: {
                    address: address,
                    key: process.env.GOOGLE_MAPS_API_KEY
                }
            });

            const results = response.data.results;
            addToCache(geocodeCache, cacheKey, results);
            return results;
        });
    });

    server.on('reverseGeocode', async (params) => {
        const { lat, lng, batch = false } = params;
        
        if (!validateLatLng({ lat, lng })) {
            throw new Error('Invalid latitude or longitude');
        }

        const cacheKey = `reverse:${lat},${lng}`;

        return withErrorHandling(async () => {
            // Check cache first
            const cached = getFromCache(geocodeCache, cacheKey);
            if (cached) return cached;

            // Handle batch requests
            if (batch) {
                return addToBatch('reverseGeocoding', { lat, lng });
            }

            const response = await client.reverseGeocode({
                params: {
                    latlng: { lat, lng },
                    key: process.env.GOOGLE_MAPS_API_KEY
                }
            });

            const results = response.data.results;
            addToCache(geocodeCache, cacheKey, results);
            return results;
        });
    });

    server.on('placeSearch', async (params) => {
        const { 
            query, 
            location, 
            radius = DEFAULT_SEARCH_RADIUS,
            type,
            minRating,
            openNow,
            rankBy = 'prominence'
        } = params;

        if (location && !validateLatLng(location)) {
            throw new Error('Invalid location coordinates');
        }

        const cacheKey = `places:${query}:${JSON.stringify(location)}:${radius}:${type}:${openNow}:${rankBy}`;

        return withErrorHandling(async () => {
            // Check cache first
            const cached = getFromCache(placesCache, cacheKey);
            if (cached) return cached;

            const response = await client.placesNearby({
                params: {
                    location: location,
                    radius: radius,
                    keyword: query,
                    type: type,
                    rankby: rankBy,
                    opennow: openNow,
                    key: process.env.GOOGLE_MAPS_API_KEY
                }
            });

            let results = response.data.results;

            // Apply additional filters
            if (minRating) {
                results = results.filter(place => 
                    place.rating >= minRating
                );
            }

            // Format results
            const formattedResults = results.map(formatPlaceResult);
            
            // Cache results
            addToCache(placesCache, cacheKey, formattedResults);
            return formattedResults;
        });
    });

    // Batch processing endpoint
    server.on('processBatch', async (params) => {
        const { batchKey } = params;
        return processBatch(batchKey);
    });

    // Cache management endpoints
    server.on('clearCache', async (params) => {
        const { type } = params;
        switch (type) {
            case 'geocode':
                geocodeCache.clear();
                break;
            case 'places':
                placesCache.clear();
                break;
            default:
                geocodeCache.clear();
                placesCache.clear();
        }
        return { success: true };
    });

    // Health check endpoint
    server.on('health', async () => {
        return { 
            status: 'healthy',
            version: '1.0.0',
            geocodeCacheSize: geocodeCache.size,
            placesCacheSize: placesCache.size,
            pendingBatches: pendingBatches.size
        };
    });

    // Error handler
    server.on('error', (error) => {
        console.error('Server error:', error);
        // Implement error reporting/monitoring here
    });

    // Start the server
    await server.start();
    console.log('Maps MCP Server started successfully');
};

// Start server with error handling
startServer().catch(error => {
    console.error('Failed to start server:', error);
    process.exit(1);
});
