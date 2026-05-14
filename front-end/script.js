// ===== CONFIGURATION =====
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    ANIMATION_DELAY: 100, // milliseconds between form group animations
    NOTIFICATION_DURATION: 4000 // milliseconds
};

// ===== MAIN APPLICATION =====
class ChurnPredictor {
    constructor() {
        this.form = document.getElementById('churnForm');
        this.predictBtn = document.getElementById('predictBtn');
        this.loading = document.getElementById('loading');
        this.result = document.getElementById('result');
        this.resultContent = document.getElementById('resultContent');
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.animateFormGroups();
        this.checkAPIHealth();
    }

    setupEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // Page load
        window.addEventListener('load', () => this.onPageLoad());
    }

    animateFormGroups() {
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach((group, index) => {
            group.style.animationDelay = `${index * CONFIG.ANIMATION_DELAY}ms`;
        });
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        try {
            this.showLoading();
            const formData = this.collectFormData();
            const result = await this.makeAPICall(formData);
            this.showResult(result, 'success');
        } catch (error) {
            this.showResult({
                error: error.message || 'An unexpected error occurred'
            }, 'error');
        } finally {
            this.hideLoading();
        }
    }

    collectFormData() {
        const formElements = {
            CreditScore: 'creditScore',
            Geography: 'geography',
            Gender: 'gender',
            Age: 'age',
            Tenure: 'tenure',
            Balance: 'balance',
            NumOfProducts: 'numProducts',
            HasCrCard: 'hasCrCard',
            IsActiveMember: 'isActiveMember',
            EstimatedSalary: 'estimatedSalary',
            Satisfaction_Score: 'satisfactionScore',
            Card_Type: 'cardType',
            Point_Earned: 'pointEarned'
        };

        const formData = {};

        for (const [apiKey, elementId] of Object.entries(formElements)) {
            const element = document.getElementById(elementId);
            if (!element) {
                throw new Error(`Form element with ID '${elementId}' not found`);
            }

            const value = element.value;
            if (!value) {
                throw new Error(`Please fill in the ${element.labels[0]?.textContent || elementId} field`);
            }

            // Convert to appropriate data type
            if (['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 
                 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 
                 'Satisfaction_Score', 'Point_Earned'].includes(apiKey)) {
                formData[apiKey] = parseFloat(value);
            } else {
                formData[apiKey] = value;
            }
        }

        return formData;
    }

    async makeAPICall(formData) {
        const response = await fetch(`${CONFIG.API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                data: [formData]
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    showLoading() {
        this.loading.style.display = 'block';
        this.result.style.display = 'none';
        this.predictBtn.disabled = true;
        this.predictBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }

    hideLoading() {
        this.loading.style.display = 'none';
        this.predictBtn.disabled = false;
        this.predictBtn.innerHTML = '<i class="fas fa-brain"></i> Analyze Customer Risk';
    }

    showResult(data, type) {
        this.result.className = `result ${type}`;
        
        if (type === 'success') {
            this.resultContent.innerHTML = this.generateSuccessHTML(data);
        } else {
            this.resultContent.innerHTML = this.generateErrorHTML(data);
        }
        
        this.result.style.display = 'block';
        this.result.scrollIntoView({ behavior: 'smooth' });
    }

    generateSuccessHTML(data) {
        const prediction = data.predictions[0];
        const willChurn = prediction.prediction === 1;
        
        return `
            <div style="text-align: center;">
                <h2><i class="fas fa-chart-line"></i> Prediction Results</h2>
                <div class="churn-result">
                    ${willChurn ? '🚨 HIGH CHURN RISK' : '✅ CUSTOMER WILL STAY'}
                </div>
                
                <div class="result-details">
                    <div class="detail-item">
                        <h4><i class="fas fa-user"></i> Customer ID</h4>
                        <p><strong>#${String(prediction.customer_id || prediction.customer_index).padStart(4, '0')}</strong></p>
                    </div>
                    
                    <div class="detail-item">
                        <h4><i class="fas fa-prediction"></i> Prediction</h4>
                        <p><strong>${willChurn ? 'Will Leave' : 'Will Stay'}</strong></p>
                    </div>
                    
                    <div class="detail-item">
                        <h4><i class="fas fa-exclamation-triangle"></i> Risk Level</h4>
                        <p><strong>${willChurn ? 'HIGH ⚠️' : 'LOW ✅'}</strong></p>
                    </div>
                    
                    <div class="detail-item">
                        <h4><i class="fas fa-lightbulb"></i> Confidence</h4>
                        <p><strong>${prediction.confidence || 'High'}</strong></p>
                    </div>
                </div>
                
                <div style="margin-top: 30px; padding: 25px; background: rgba(255,255,255,0.7); border-radius: 15px;">
                    <h3><i class="fas fa-bullseye"></i> ${willChurn ? 'Retention Strategy' : 'Engagement Strategy'}</h3>
                    <p style="margin-top: 15px; font-size: 1.1em; line-height: 1.6;">
                        ${willChurn ? 
                            '🎯 <strong>Immediate Action Required:</strong><br>• Offer personalized retention incentives<br>• Schedule one-on-one customer consultation<br>• Review service satisfaction<br>• Consider account upgrade offers' : 
                            '🌟 <strong>Maintain Excellence:</strong><br>• Continue providing exceptional service<br>• Explore upselling opportunities<br>• Gather feedback for improvement<br>• Reward loyalty with exclusive benefits'
                        }
                    </p>
                </div>
            </div>
        `;
    }

    generateErrorHTML(data) {
        return `
            <div style="text-align: center;">
                <h2><i class="fas fa-exclamation-triangle"></i> Error Occurred</h2>
                <div class="churn-result" style="font-size: 1.8em;">
                    ❌ Prediction Failed
                </div>
                <p style="font-size: 1.1em; margin-top: 20px;">${data.error}</p>
                <div style="margin-top: 25px; padding: 20px; background: rgba(255,255,255,0.5); border-radius: 10px;">
                    <p><strong>💡 Troubleshooting:</strong></p>
                    <ul style="text-align: left; margin-top: 10px;">
                        <li>Make sure FastAPI server is running</li>
                        <li>Check if all form fields are filled correctly</li>
                        <li>Verify API endpoint is accessible at ${CONFIG.API_BASE_URL}</li>
                        <li>Check browser console for additional errors</li>
                    </ul>
                </div>
            </div>
        `;
    }

    async checkAPIHealth() {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
            if (response.ok) {
                console.log('✅ API is running and ready');
                this.showNotification('🟢 API Connected Successfully', 'success');
            } else {
                console.log('⚠️ API health check failed');
                this.showNotification('🟡 API Connection Issues', 'warning');
            }
        } catch (error) {
            console.log('❌ Cannot connect to API:', error);
            this.showNotification('🔴 API Not Available - Please start your FastAPI server', 'error');
        }
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            font-weight: 600;
            z-index: 1000;
            animation: slideInNotification 0.5s ease;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            max-width: 400px;
            font-family: 'Poppins', sans-serif;
        `;
        
        // Set background based on type
        const backgrounds = {
            success: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            warning: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
            error: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        };
        
        notification.style.background = backgrounds[type] || backgrounds.error;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutNotification 0.5s ease';
            setTimeout(() => notification.remove(), 500);
        }, CONFIG.NOTIFICATION_DURATION);
    }

    onPageLoad() {
        console.log('🏦 Bank Churn Predictor initialized');
        console.log(`📡 API Endpoint: ${CONFIG.API_BASE_URL}`);
    }
}

// ===== UTILITY FUNCTIONS =====
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function validateFormData(data) {
    const requiredFields = [
        'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance',
        'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
        'Satisfaction_Score', 'Card_Type', 'Point_Earned'
    ];

    for (const field of requiredFields) {
        if (!data.hasOwnProperty(field) || data[field] === '' || data[field] === null) {
            throw new Error(`Field '${field}' is required`);
        }
    }

    // Additional validation
    if (data.CreditScore < 300 || data.CreditScore > 850) {
        throw new Error('Credit Score must be between 300 and 850');
    }

    if (data.Age < 18 || data.Age > 100) {
        throw new Error('Age must be between 18 and 100');
    }

    if (data.Balance < 0) {
        throw new Error('Account Balance cannot be negative');
    }

    return true;
}

// ===== APPLICATION STARTUP =====
document.addEventListener('DOMContentLoaded', () => {
    new ChurnPredictor();
});

// ===== GLOBAL ERROR HANDLING =====
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});