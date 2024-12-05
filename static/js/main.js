document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const fileCount = document.getElementById('file-count');
    const resultsDiv = document.getElementById('results');
    const analyzeButton = document.querySelector('.analyze-button');
    let progressBar;

    fileInput.addEventListener('change', function() {
        const count = this.files.length;
        if (count > 0) {
            fileCount.textContent = `已选择 ${count} 个文件`;
            analyzeButton.disabled = false;
        } else {
            fileCount.textContent = '';
            analyzeButton.disabled = true;
        }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!fileInput.files.length) {
            alert('请选择至少一个文件');
            return;
        }

        progressBar = createProgressBar();
        analyzeButton.disabled = true;

        const formData = new FormData();
        for (let file of fileInput.files) {
            formData.append('files[]', file);
        }

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                displayResults(data);
            } else {
                throw new Error(data.error || '分析过程中发生错误');
            }
        } catch (error) {
            alert(error.message);
            console.error('Error:', error);
        } finally {
            if (progressBar) {
                progressBar.remove();
            }
            analyzeButton.disabled = false;
        }
    });

    function createProgressBar() {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'progress-container';
        
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        
        progressContainer.appendChild(progressBar);
        form.appendChild(progressContainer);
        
        setTimeout(() => {
            progressBar.style.width = '100%';
        }, 100);
        
        return progressContainer;
    }

    function displayResults(data) {
        if (!resultsDiv) return;

        resultsDiv.innerHTML = '';
        
        const resultContent = document.createElement('div');
        resultContent.className = 'result-content';

        // 创建颜色展示区域
        const colorsDiv = document.createElement('div');
        colorsDiv.className = 'colors-display';

        // 主色调区域
        const primaryDiv = document.createElement('div');
        primaryDiv.className = 'color-section';
        primaryDiv.innerHTML = '<h3>主色调</h3>';
        
        if (data.primary_colors && Array.isArray(data.primary_colors)) {
            data.primary_colors.forEach(color => {
                if (color && color.rgb) {
                    const colorBox = createColorBox(color);
                    primaryDiv.appendChild(colorBox);
                }
            });
        }

        // 辅助色区域
        const secondaryDiv = document.createElement('div');
        secondaryDiv.className = 'color-section';
        secondaryDiv.innerHTML = '<h3>辅助色</h3>';
        
        if (data.secondary_colors && Array.isArray(data.secondary_colors)) {
            data.secondary_colors.forEach(color => {
                if (color && color.rgb) {
                    const colorBox = createColorBox(color);
                    secondaryDiv.appendChild(colorBox);
                }
            });
        }

        colorsDiv.appendChild(primaryDiv);
        colorsDiv.appendChild(secondaryDiv);
        resultContent.appendChild(colorsDiv);

        // 添加图表
        if (data.plot) {
            const plotImg = document.createElement('img');
            plotImg.src = 'data:image/png;base64,' + data.plot;
            plotImg.className = 'result-plot';
            resultContent.appendChild(plotImg);
        }

        resultsDiv.appendChild(resultContent);
        resultsDiv.style.display = 'block';
    }

    function createColorBox(color) {
        const box = document.createElement('div');
        box.className = 'color-box';
        
        const colorInfo = document.createElement('div');
        colorInfo.className = 'color-info';
        colorInfo.textContent = `RGB(${color.rgb.join(', ')}) ${color.percentage.toFixed(1)}%`;
        
        box.appendChild(colorInfo);
        return box;
    }
});