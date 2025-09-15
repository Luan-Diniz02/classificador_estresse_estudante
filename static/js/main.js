/**
 * JavaScript principal para o Classificador de Estresse Acadêmico
 */

// Configurações globais
const CONFIG = {
    API_BASE_URL: '/api',
    CHART_COLORS: {
        primary: '#0d6efd',
        success: '#198754',
        warning: '#ffc107',
        danger: '#dc3545',
        info: '#0dcaf0'
    },
    ANIMATION_DURATION: 300
};

// Utilitários globais
const Utils = {
    /**
     * Debounce function para otimizar performance
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Formatar números para exibição
     */
    formatNumber: function(num, decimals = 2) {
        return parseFloat(num).toFixed(decimals);
    },

    /**
     * Validar campos obrigatórios de um formulário
     */
    validateRequiredFields: function(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        let firstInvalidField = null;

        requiredFields.forEach(field => {
            const value = field.value.trim();
            if (!value) {
                field.classList.add('is-invalid');
                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });

        if (firstInvalidField) {
            firstInvalidField.focus();
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        return isValid;
    },

    /**
     * Mostrar notificação toast
     */
    showToast: function(message, type = 'info', duration = 5000) {
        // Criar elemento do toast
        const toastId = 'toast-' + Date.now();
        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" 
                 role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="${duration}">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="bi bi-${this.getToastIcon(type)} me-2"></i>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                            data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Adicionar ao container de toasts
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1055';
            document.body.appendChild(toastContainer);
        }

        toastContainer.insertAdjacentHTML('beforeend', toastHTML);

        // Inicializar e mostrar toast
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();

        // Remover elemento após ser escondido
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    },

    /**
     * Obter ícone para toast baseado no tipo
     */
    getToastIcon: function(type) {
        const icons = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    /**
     * Fazer requisição AJAX
     */
    ajax: function(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        const finalOptions = { ...defaultOptions, ...options };

        return fetch(url, finalOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('AJAX Error:', error);
                Utils.showToast('Erro na comunicação com o servidor', 'danger');
                throw error;
            });
    },

    /**
     * Animar contador numérico
     */
    animateCounter: function(element, start, end, duration = 2000) {
        const startTime = performance.now();
        const range = end - start;

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Função de easing para animação suave
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = start + (range * easeOutQuart);
            
            element.textContent = Math.floor(current);

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = end;
            }
        }

        requestAnimationFrame(updateCounter);
    }
};

// Gerenciador de loading states
const LoadingManager = {
    show: function(button, text = 'Carregando...') {
        if (button.hasAttribute('data-original-text')) return;
        
        button.setAttribute('data-original-text', button.innerHTML);
        button.innerHTML = `<span class="loading">${text}</span>`;
        button.disabled = true;
    },

    hide: function(button) {
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
            button.removeAttribute('data-original-text');
            button.disabled = false;
        }
    }
};

// Gerenciador de formulários
const FormManager = {
    /**
     * Inicializar validação em tempo real
     */
    initRealTimeValidation: function(form) {
        const fields = form.querySelectorAll('input, select, textarea');
        
        fields.forEach(field => {
            field.addEventListener('blur', () => {
                this.validateField(field);
            });

            field.addEventListener('input', Utils.debounce(() => {
                if (field.classList.contains('is-invalid')) {
                    this.validateField(field);
                }
            }, 500));
        });
    },

    /**
     * Validar campo individual
     */
    validateField: function(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        
        if (isRequired && !value) {
            this.setFieldInvalid(field, 'Este campo é obrigatório');
            return false;
        }

        // Validações específicas por tipo
        if (field.type === 'email' && value && !this.isValidEmail(value)) {
            this.setFieldInvalid(field, 'Email inválido');
            return false;
        }

        if (field.type === 'number' && value) {
            const min = field.getAttribute('min');
            const max = field.getAttribute('max');
            
            if (min && parseFloat(value) < parseFloat(min)) {
                this.setFieldInvalid(field, `Valor mínimo: ${min}`);
                return false;
            }
            
            if (max && parseFloat(value) > parseFloat(max)) {
                this.setFieldInvalid(field, `Valor máximo: ${max}`);
                return false;
            }
        }

        this.setFieldValid(field);
        return true;
    },

    /**
     * Marcar campo como inválido
     */
    setFieldInvalid: function(field, message) {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    },

    /**
     * Marcar campo como válido
     */
    setFieldValid: function(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    },

    /**
     * Validar email
     */
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    /**
     * Limpar validações do formulário
     */
    clearValidation: function(form) {
        const fields = form.querySelectorAll('.is-valid, .is-invalid');
        fields.forEach(field => {
            field.classList.remove('is-valid', 'is-invalid');
        });

        const feedbacks = form.querySelectorAll('.invalid-feedback');
        feedbacks.forEach(feedback => feedback.remove());
    }
};

// Gerenciador de gráficos
const ChartManager = {
    /**
     * Configurações padrão para gráficos Plotly
     */
    defaultLayout: {
        font: { 
            family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
            size: 12
        },
        margin: { l: 50, r: 50, t: 50, b: 50 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        showlegend: true
    },

    defaultConfig: {
        responsive: true,
        displayModeBar: false
    },

    /**
     * Renderizar gráfico com loading
     */
    renderChart: function(elementId, data, layout = {}, config = {}) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.error(`Elemento ${elementId} não encontrado`);
            return;
        }

        // Mostrar loading
        element.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading">Carregando gráfico...</div></div>';

        // Mesclar configurações
        const finalLayout = { ...this.defaultLayout, ...layout };
        const finalConfig = { ...this.defaultConfig, ...config };

        // Renderizar após pequeno delay para UX
        setTimeout(() => {
            try {
                Plotly.newPlot(elementId, data, finalLayout, finalConfig);
            } catch (error) {
                console.error('Erro ao renderizar gráfico:', error);
                element.innerHTML = '<div class="text-center text-muted"><i class="bi bi-exclamation-circle fs-1"></i><p>Erro ao carregar gráfico</p></div>';
            }
        }, 100);
    }
};

// Inicialização quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('🧠 Classificador de Estresse Acadêmico - Frontend carregado');

    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers do Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Inicializar validação em formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        FormManager.initRealTimeValidation(form);
    });

    // Auto-hide alerts após 10 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 10000);
    });

    // Animar elementos com classe fade-in quando entram na viewport
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.slide-in-up, .fade-in-delayed');
    animatedElements.forEach(el => observer.observe(el));

    // Smooth scroll para âncoras
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Atualizar ano no footer
    const currentYear = new Date().getFullYear();
    const yearElements = document.querySelectorAll('.current-year');
    yearElements.forEach(el => el.textContent = currentYear);

    // Debug mode para desenvolvimento
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('🔧 Modo de desenvolvimento ativado');
        window.Utils = Utils;
        window.FormManager = FormManager;
        window.ChartManager = ChartManager;
        window.LoadingManager = LoadingManager;
    }
});

// Funcionalidade específica para upload de arquivos
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const feedback = this.parentNode.querySelector('.file-feedback');
            
            // Remover feedback anterior
            if (feedback) feedback.remove();
            
            if (file) {
                const fileSize = (file.size / 1024 / 1024).toFixed(2); // MB
                const fileName = file.name;
                
                // Criar elemento de feedback
                const feedbackEl = document.createElement('div');
                feedbackEl.className = 'file-feedback mt-2 small text-muted';
                feedbackEl.innerHTML = `
                    <i class="bi bi-file-earmark-check text-success"></i>
                    <strong>${fileName}</strong> (${fileSize} MB)
                `;
                
                this.parentNode.appendChild(feedbackEl);
            }
        });
    });
});

// Service Worker para cache (PWA - opcional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Comentado para não implementar agora, mas preparado para futuro
        // navigator.serviceWorker.register('/sw.js')
        //     .then(function(registration) {
        //         console.log('SW registrado com sucesso:', registration.scope);
        //     })
        //     .catch(function(error) {
        //         console.log('Falha ao registrar SW:', error);
        //     });
    });
}

// Exportar para uso global (se necessário)
window.ClassifierApp = {
    Utils,
    FormManager,
    ChartManager,
    LoadingManager,
    CONFIG
};