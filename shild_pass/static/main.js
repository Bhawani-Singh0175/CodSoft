document.addEventListener('DOMContentLoaded', () => {
    const lengthSlider = document.getElementById('length-slider');
    const lengthDisplay = document.getElementById('length-display');
    const generateBtn = document.getElementById('generate-btn');
    const copyBtn = document.getElementById('copy-btn');
    const passwordDisplay = document.getElementById('password-display');
    const toast = document.getElementById('toast');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history');
    
    // Toggles
    const toggleUpper = document.getElementById('toggle-upper');
    const toggleLower = document.getElementById('toggle-lower');
    const toggleNumbers = document.getElementById('toggle-numbers');
    const toggleSpecial = document.getElementById('toggle-special');

    // Strength elements
    const strengthText = document.getElementById('strength-text');
    const bars = [
        document.getElementById('bar-1'),
        document.getElementById('bar-2'),
        document.getElementById('bar-3'),
        document.getElementById('bar-4')
    ];

    let history = JSON.parse(localStorage.getItem('passforge_history')) || [];

    // Initialize UI
    updateHistoryUI();
    generatePassword(); // Generate one on load

    // Events
    lengthSlider.addEventListener('input', (e) => {
        lengthDisplay.textContent = e.target.value;
    });

    generateBtn.addEventListener('click', generatePassword);

    copyBtn.addEventListener('click', async () => {
        const pwd = passwordDisplay.value;
        if (!pwd || pwd.includes('Click generate')) return;
        
        try {
            await navigator.clipboard.writeText(pwd);
            showToast();
        } catch (err) {
            console.error('Failed to copy', err);
        }
    });

    clearHistoryBtn.addEventListener('click', () => {
        history = [];
        localStorage.removeItem('passforge_history');
        updateHistoryUI();
    });

    // Main API call
    async function generatePassword() {
        // Enforce at least one toggle
        if (!toggleUpper.checked && !toggleLower.checked && !toggleNumbers.checked && !toggleSpecial.checked) {
            toggleLower.checked = true;
        }

        const payload = {
            length: lengthSlider.value,
            uppercase: toggleUpper.checked,
            lowercase: toggleLower.checked,
            numbers: toggleNumbers.checked,
            special: toggleSpecial.checked
        };

        try {
            const res = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            passwordDisplay.value = data.password;
            updateStrengthUI(data.strength);
            addToHistory(data.password);
            
        } catch (error) {
            console.error("Error generating password:", error);
            passwordDisplay.value = "Error generating password";
        }
    }

    function updateStrengthUI(strength) {
        strengthText.textContent = strength;
        
        // Reset colors
        bars.forEach(bar => bar.style.backgroundColor = 'var(--border-color)');
        strengthText.style.color = 'var(--text-muted)';

        let activeBars = 0;
        let color = '';

        switch(strength) {
            case 'Weak':
                activeBars = 1;
                color = '#ef4444'; // Red
                break;
            case 'Medium':
                activeBars = 2;
                color = '#f59e0b'; // Amber
                break;
            case 'Strong':
                activeBars = 3;
                color = '#10b981'; // Emerald
                break;
            case 'Very Strong':
                activeBars = 4;
                color = '#059669'; // Darker Emerald
                break;
        }

        strengthText.style.color = color;
        for(let i = 0; i < activeBars; i++) {
            bars[i].style.backgroundColor = color;
        }
    }

    function addToHistory(pwd) {
        // Avoid consecutive duplicates
        if (history.length > 0 && history[0] === pwd) return;
        
        history.unshift(pwd);
        if (history.length > 5) {
            history.pop();
        }
        
        localStorage.setItem('passforge_history', JSON.stringify(history));
        updateHistoryUI();
    }

    function updateHistoryUI() {
        historyList.innerHTML = '';
        if (history.length === 0) {
            historyList.innerHTML = '<li style="color: var(--text-muted); font-size: 0.9rem;">No history yet</li>';
            return;
        }

        history.forEach(pwd => {
            const li = document.createElement('li');
            li.className = 'history-item stitch-border';
            
            const span = document.createElement('span');
            span.className = 'history-pwd';
            // Show only first 8 chars then ellipses for security/space
            span.textContent = pwd.length > 12 ? pwd.substring(0, 10) + '...' : pwd;
            
            const copyIcon = document.createElement('div');
            copyIcon.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--primary-color)" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
            copyIcon.style.cursor = 'pointer';
            copyIcon.title = 'Copy this password';
            
            copyIcon.addEventListener('click', async () => {
                await navigator.clipboard.writeText(pwd);
                showToast();
            });

            li.appendChild(span);
            li.appendChild(copyIcon);
            historyList.appendChild(li);
        });
    }

    function showToast() {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }
});
