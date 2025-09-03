/**
 * QBTC Commercial Website - Main JavaScript
 * Funcionalidades interactivas para el sitio web comercial
 */

document.addEventListener('DOMContentLoaded', function() {
    // Animaciones de scroll suave
    initSmoothScrolling();
    
    // Efectos de partículas
    initParticleEffects();
    
    // Manejo de formularios
    initFormHandling();
    
    // Efectos de hover en servicios
    initServiceEffects();
    
    // Contador de stats animado
    initStatsCounter();
    
    console.log('🚀 QBTC Commercial Website iniciado');
});

function initSmoothScrolling() {
    // Scroll suave para enlaces de navegación
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initParticleEffects() {
    // Crear partículas flotantes en el header
    const header = document.querySelector('header');
    if (header) {
        for (let i = 0; i < 20; i++) {
            createFloatingParticle(header);
        }
    }
}

function createFloatingParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'floating-particle';
    particle.style.cssText = `
        position: absolute;
        width: ${Math.random() * 4 + 2}px;
        height: ${Math.random() * 4 + 2}px;
        background: rgba(0, 255, 255, ${Math.random() * 0.5 + 0.3});
        border-radius: 50%;
        pointer-events: none;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: float ${Math.random() * 10 + 10}s infinite linear;
    `;
    container.appendChild(particle);
    
    // Remover partícula después de la animación
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 20000);
}

function initFormHandling() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Mostrar estado de carga
            submitButton.textContent = 'Enviando...';
            submitButton.disabled = true;
            
            try {
                // Recopilar datos del formulario
                const formData = new FormData(form);
                const data = Object.fromEntries(formData.entries());
                
                // Agregar datos adicionales
                data.timestamp = new Date().toISOString();
                data.userAgent = navigator.userAgent;
                data.url = window.location.href;
                
                // Simular envío (en producción conectar con backend real)
                await simulateFormSubmission(data);
                
                // Mostrar mensaje de éxito
                showNotification('✅ Consulta enviada correctamente. Nos pondremos en contacto pronto.', 'success');
                form.reset();
                
            } catch (error) {
                console.error('Error enviando formulario:', error);
                showNotification('❌ Error al enviar la consulta. Por favor intente nuevamente.', 'error');
            } finally {
                // Restaurar botón
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });
    });
}

async function simulateFormSubmission(data) {
    // Simular delay de red
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Log de la consulta (en producción enviar a backend)
    console.log('📩 Nueva consulta:', data);
    
    // Simular respuesta del servidor
    if (Math.random() > 0.1) {
        return { success: true, id: Math.random().toString(36).substr(2, 9) };
    } else {
        throw new Error('Simulación de error de red');
    }
}

function showNotification(message, type = 'info') {
    // Crear notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#00ff88' : type === 'error' ? '#ff4444' : '#00ffff'};
        color: #000;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        font-weight: bold;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 350px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animación de entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function initServiceEffects() {
    const services = document.querySelectorAll('.service');
    
    services.forEach(service => {
        service.addEventListener('mouseenter', function() {
            // Efecto de resplandor
            this.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.4)';
            
            // Agregar partículas temporales
            for (let i = 0; i < 5; i++) {
                setTimeout(() => createServiceParticle(this), i * 100);
            }
        });
        
        service.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
}

function createServiceParticle(service) {
    const particle = document.createElement('div');
    particle.style.cssText = `
        position: absolute;
        width: 3px;
        height: 3px;
        background: #00ffff;
        border-radius: 50%;
        pointer-events: none;
        left: ${Math.random() * service.offsetWidth}px;
        top: ${Math.random() * service.offsetHeight}px;
        opacity: 1;
        transition: all 1s ease-out;
    `;
    
    service.style.position = 'relative';
    service.appendChild(particle);
    
    // Animar partícula
    setTimeout(() => {
        particle.style.transform = `translate(${(Math.random() - 0.5) * 100}px, ${-Math.random() * 50}px)`;
        particle.style.opacity = '0';
    }, 50);
    
    // Remover partícula
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 1050);
}

function initStatsCounter() {
    // Agregar contador de estadísticas si existe una sección para ello
    const statsSection = document.querySelector('#stats');
    if (statsSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateStats();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(statsSection);
    }
}

function animateStats() {
    const stats = [
        { element: '.stat-clients', target: 500, suffix: '+' },
        { element: '.stat-threats', target: 1000000, suffix: '+' },
        { element: '.stat-uptime', target: 99.9, suffix: '%' },
        { element: '.stat-response', target: 24, suffix: 'h' }
    ];
    
    stats.forEach(stat => {
        const element = document.querySelector(stat.element);
        if (element) {
            animateCounter(element, 0, stat.target, stat.suffix, 2000);
        }
    });
}

function animateCounter(element, start, end, suffix, duration) {
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = start + (end - start) * easeOutQuart(progress);
        const value = suffix === '%' ? current.toFixed(1) : Math.floor(current);
        
        element.textContent = value + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
}

// Agregar CSS dinámico para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    .notification {
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(400px); }
        to { transform: translateX(0); }
    }
    
    .service {
        transition: all 0.3s ease;
    }
    
    .floating-particle {
        z-index: 1;
    }
`;
document.head.appendChild(style);

// Funciones de utilidad
window.QBTCCommercial = {
    showNotification,
    createFloatingParticle,
    animateCounter
};
