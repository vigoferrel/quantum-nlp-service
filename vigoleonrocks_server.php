<?php
/**
 * VIGOLEONROCKS - Servidor PHP Básico
 * Sistema de IA Cuántica
 */

// Configuración
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Función para obtener timestamp
function getTimestamp() {
    return date('c'); // ISO 8601 format
}

// Función para calcular uptime (simulado)
function getUptime() {
    $start = strtotime('2025-01-01 00:00:00');
    $now = time();
    $diff = $now - $start;

    $days = floor($diff / 86400);
    $hours = floor(($diff % 86400) / 3600);
    $minutes = floor(($diff % 3600) / 60);

    return "{$days} days, {$hours} hours, {$minutes} minutes";
}

// Routing básico
$request_uri = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

// Remover query string
$path = parse_url($request_uri, PHP_URL_PATH);

// Routing
switch ($path) {
    case '/':
    case '/index.php':
        handleHome();
        break;

    case '/api/status':
        handleStatus();
        break;

    case '/api/test':
        handleTest();
        break;

    case '/api/info':
        handleInfo();
        break;

    default:
        handleNotFound();
        break;
}

function handleHome() {
    $response = [
        'message' => 'VIGOLEONROCKS - Sistema de IA Cuántica',
        'status' => 'active',
        'version' => '1.0-php',
        'timestamp' => getTimestamp(),
        'description' => 'Sistema de IA con respuestas humanas naturales',
        'endpoints' => [
            'GET /' => 'Página principal',
            'GET /api/status' => 'Estado del sistema',
            'GET /api/test' => 'Test de funcionalidad',
            'GET /api/info' => 'Información del sistema'
        ]
    ];

    echo json_encode($response, JSON_PRETTY_PRINT);
}

function handleStatus() {
    $response = [
        'status' => 'online',
        'server' => 'VIGOLEONROCKS',
        'version' => '1.0-php',
        'uptime' => getUptime(),
        'timestamp' => getTimestamp(),
        'message' => 'Sistema funcionando correctamente',
        'php_version' => PHP_VERSION,
        'server_info' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown'
    ];

    echo json_encode($response, JSON_PRETTY_PRINT);
}

function handleTest() {
    $response = [
        'test' => 'ok',
        'timestamp' => getTimestamp(),
        'message' => 'API de test funcionando correctamente',
        'random_number' => rand(1, 100),
        'server_time' => date('Y-m-d H:i:s'),
        'request_method' => $_SERVER['REQUEST_METHOD'],
        'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown'
    ];

    echo json_encode($response, JSON_PRETTY_PRINT);
}

function handleInfo() {
    $response = [
        'system_info' => [
            'php_version' => PHP_VERSION,
            'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown',
            'server_name' => $_SERVER['SERVER_NAME'] ?? 'Unknown',
            'server_port' => $_SERVER['SERVER_PORT'] ?? 'Unknown',
            'document_root' => $_SERVER['DOCUMENT_ROOT'] ?? 'Unknown',
            'script_filename' => $_SERVER['SCRIPT_FILENAME'] ?? 'Unknown'
        ],
        'vigoleonrocks_info' => [
            'name' => 'VIGOLEONROCKS',
            'version' => '1.0-php',
            'description' => 'Sistema de IA Cuántica con respuestas humanas naturales',
            'features' => [
                'Procesamiento de lenguaje natural',
                'Respuestas empáticas',
                'Análisis arquetipal',
                'Traducción multilingüe',
                'Sistema cuántico simulado'
            ],
            'technologies' => [
                'PHP ' . PHP_VERSION,
                'JSON API',
                'RESTful endpoints',
                'CORS enabled'
            ]
        ],
        'timestamp' => getTimestamp()
    ];

    echo json_encode($response, JSON_PRETTY_PRINT);
}

function handleNotFound() {
    http_response_code(404);
    $response = [
        'error' => 'Endpoint not found',
        'message' => 'El endpoint solicitado no existe',
        'available_endpoints' => [
            'GET /' => 'Página principal',
            'GET /api/status' => 'Estado del sistema',
            'GET /api/test' => 'Test de funcionalidad',
            'GET /api/info' => 'Información del sistema'
        ],
        'timestamp' => getTimestamp()
    ];

    echo json_encode($response, JSON_PRETTY_PRINT);
}
?>