        // Tab switching functionality
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.dataset.tab;
                
                // Update active tab button
                document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Update active tab pane
                document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
                document.getElementById(targetTab).classList.add('active');
            });
        });

        // Slider creation function
        function createSlider(container, label, min, max, defaultValue, unit = '') {
            const sliderContainer = document.createElement('div');
            sliderContainer.className = 'slider-container';
            
            sliderContainer.innerHTML = `
                <div class="slider-header">
                    <span class="slider-label">${label}</span>
                    <span class="slider-value">${defaultValue.toFixed(2)}${unit}</span>
                </div>
                <input type="range" class="slider" min="${min}" max="${max}" step="0.01" value="${defaultValue}">
            `;
            
            const slider = sliderContainer.querySelector('.slider');
            const valueDisplay = sliderContainer.querySelector('.slider-value');
            
            slider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                valueDisplay.textContent = value.toFixed(2) + unit;
            });
            
            container.appendChild(sliderContainer);
            return slider;
        }

        // Initialize sliders
        const movementSliders = document.getElementById('movement-sliders');
        const antiAfkSliders = document.getElementById('anti-afk-sliders');

        // Movement sliders
        createSlider(movementSliders, 'Look Intensity', 0, 3, 1.5);
        createSlider(movementSliders, 'Move Intensity', 0, 2, 0.3);
        createSlider(movementSliders, 'Forward Intensity', 0, 2, 1.0);
        createSlider(movementSliders, 'Jump Chance', 0, 1, 0.15);
        createSlider(movementSliders, 'Jump Interval', 1, 10, 3.0, 's');
        createSlider(movementSliders, 'Weapon Switch Chance', 0, 1, 0.1);
        createSlider(movementSliders, 'Weapon Switch Interval', 1, 15, 5.0, 's');
        createSlider(movementSliders, 'Min Movement Duration', 1, 10, 2.0, 's');
        createSlider(movementSliders, 'Max Movement Duration', 2, 15, 8.0, 's');
        createSlider(movementSliders, 'Min Break Duration', 1, 10, 3.0, 's');
        createSlider(movementSliders, 'Max Break Duration', 2, 20, 12.0, 's');

        // Anti-AFK sliders
        createSlider(antiAfkSliders, 'Interval', 10, 120, 60.0, 's');
        createSlider(antiAfkSliders, 'Right Bumper Duration', 0.1, 1, 0.1, 's');
        createSlider(antiAfkSliders, 'Left Bumper Duration', 0.1, 1, 0.2, 's');
        createSlider(antiAfkSliders, 'Delay Between Buttons', 0.1, 2, 1.0, 's');

        // Log function
        function addLog(message, type = 'info') {
            const logContainer = document.getElementById('log-container');
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry ${type}`;
            logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            logContainer.appendChild(logEntry);
            logContainer.scrollTop = logContainer.scrollHeight;
        }

        // Button event listeners (placeholder functionality)
        document.getElementById('browser-button').addEventListener('click', () => {
            addLog('Opening Xbox sessions...', 'info');
        });

        document.getElementById('connect-button').addEventListener('click', () => {
            addLog('Connecting controller...', 'info');
        });

        // Initialize profiles count
        document.getElementById('profiles-count').textContent = 'Available Profiles: 0/20';