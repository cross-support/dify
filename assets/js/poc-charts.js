// PoC報告書用のチャート生成スクリプト

document.addEventListener('DOMContentLoaded', function() {
    // 作業時間比較チャート
    const timeComparisonCtx = document.getElementById('timeComparisonChart');
    if (timeComparisonCtx) {
        new Chart(timeComparisonCtx, {
            type: 'bar',
            data: {
                labels: ['リサーチ', '執筆', '校正・編集', '最終チェック'],
                datasets: [{
                    label: '従来手法（時間）',
                    data: [2.0, 1.5, 1.0, 0.5],
                    backgroundColor: 'rgba(220, 53, 69, 0.8)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 2
                }, {
                    label: 'AI支援（時間）',
                    data: [0.23, 0.5, 1.5, 0.37],
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '作業時間比較（1記事あたり）',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: '時間（時間）'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + 'h';
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '作業工程'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    // ROI予測チャート
    const roiProjectionCtx = document.getElementById('roiProjectionChart');
    if (roiProjectionCtx) {
        new Chart(roiProjectionCtx, {
            type: 'line',
            data: {
                labels: ['初期', '3ヶ月', '6ヶ月', '9ヶ月', '12ヶ月', '18ヶ月', '24ヶ月'],
                datasets: [{
                    label: '累積削減効果（万円）',
                    data: [0, 30, 65, 105, 150, 225, 300],
                    borderColor: 'rgba(40, 167, 69, 1)',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(40, 167, 69, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }, {
                    label: '累積投資額（万円）',
                    data: [50, 55, 60, 65, 70, 80, 90],
                    borderColor: 'rgba(220, 53, 69, 1)',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(220, 53, 69, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }, {
                    label: 'ROI（%）',
                    data: [-100, -45, 8, 62, 114, 181, 233],
                    borderColor: 'rgba(102, 126, 234, 1)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: false,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'ROI予測（24ヶ月）',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        position: 'top'
                    },
                    annotation: {
                        annotations: {
                            breakEven: {
                                type: 'line',
                                yMin: 0,
                                yMax: 0,
                                yScaleID: 'y1',
                                borderColor: 'rgba(255, 193, 7, 1)',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                label: {
                                    content: '損益分岐点',
                                    enabled: true,
                                    position: 'start'
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: '期間'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: '金額（万円）'
                        },
                        grid: {
                            drawOnChartArea: true,
                        },
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'ROI（%）'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 2500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    // スコアサークルのアニメーション
    const scoreCircles = document.querySelectorAll('.score-circle');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const scoreElement = entry.target.querySelector('.score');
                const finalScore = parseInt(scoreElement.textContent);
                animateScore(scoreElement, finalScore);
            }
        });
    }, { threshold: 0.5 });

    scoreCircles.forEach(circle => {
        observer.observe(circle);
    });

    function animateScore(element, finalValue) {
        let currentValue = 0;
        const increment = finalValue / 60; // 60フレームで完了
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                element.textContent = finalValue;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue);
            }
        }, 30);
    }

    // メトリクス値のアニメーション
    const metricValues = document.querySelectorAll('.metric-value');
    const metricObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const valueElement = entry.target;
                const finalValue = valueElement.textContent;

                // 数値部分を抽出
                const numericValue = parseInt(finalValue.replace(/\D/g, ''));

                if (!isNaN(numericValue)) {
                    animateMetric(valueElement, numericValue, finalValue);
                }
            }
        });
    }, { threshold: 0.5 });

    metricValues.forEach(value => {
        metricObserver.observe(value);
    });

    function animateMetric(element, numericValue, originalText) {
        let currentValue = 0;
        const increment = numericValue / 50;
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                element.textContent = originalText;
                clearInterval(timer);
            } else {
                // 元のテキストの形式を保持（%、件、分など）
                if (originalText.includes('%')) {
                    element.textContent = Math.floor(currentValue) + '%';
                } else if (originalText.includes('件')) {
                    element.textContent = Math.floor(currentValue) + '件';
                } else if (originalText.includes('分')) {
                    element.textContent = Math.floor(currentValue) + '分';
                } else {
                    element.textContent = Math.floor(currentValue);
                }
            }
        }, 40);
    }

    // ケーススタディのプログレスバー効果
    const caseMetrics = document.querySelectorAll('.case-metric');
    const caseObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInFromLeft 0.6s ease-out forwards';
            }
        });
    }, { threshold: 0.3 });

    caseMetrics.forEach(metric => {
        caseObserver.observe(metric);
    });

    // ホバーエフェクトの追加
    const assessmentCategories = document.querySelectorAll('.assessment-category');
    assessmentCategories.forEach(category => {
        category.addEventListener('mouseenter', function() {
            const scoreCircle = this.querySelector('.score-circle');
            if (scoreCircle) {
                scoreCircle.style.transform = 'scale(1.05)';
                scoreCircle.style.transition = 'transform 0.3s ease';
            }
        });

        category.addEventListener('mouseleave', function() {
            const scoreCircle = this.querySelector('.score-circle');
            if (scoreCircle) {
                scoreCircle.style.transform = 'scale(1)';
            }
        });
    });

    // カウンターのリセット機能（デバッグ用）
    window.resetCounters = function() {
        metricValues.forEach(value => {
            const originalText = value.getAttribute('data-original') || value.textContent;
            value.setAttribute('data-original', originalText);
            value.textContent = '0';
        });

        scoreCircles.forEach(circle => {
            const scoreElement = circle.querySelector('.score');
            const originalScore = scoreElement.getAttribute('data-original') || scoreElement.textContent;
            scoreElement.setAttribute('data-original', originalScore);
            scoreElement.textContent = '0';
        });
    };
});

// CSSアニメーションの追加
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInFromLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .case-study {
        animation: fadeInUp 0.6s ease-out;
    }

    .case-study:nth-child(2) {
        animation-delay: 0.2s;
    }

    .case-study:nth-child(3) {
        animation-delay: 0.4s;
    }

    .assessment-category {
        animation: fadeInUp 0.6s ease-out;
    }

    .assessment-category:nth-child(2) {
        animation-delay: 0.15s;
    }

    .assessment-category:nth-child(3) {
        animation-delay: 0.3s;
    }

    .assessment-category:nth-child(4) {
        animation-delay: 0.45s;
    }

    .recommendation {
        animation: fadeInUp 0.6s ease-out;
    }

    .recommendation.short-term {
        animation-delay: 0.2s;
    }

    .recommendation.long-term {
        animation-delay: 0.4s;
    }

    /* チャートコンテナのレスポンシブ対応 */
    .comparison-chart,
    .roi-chart {
        position: relative;
        height: 300px;
    }

    @media (max-width: 768px) {
        .comparison-chart,
        .roi-chart {
            height: 250px;
        }
    }
`;</style>

document.head.appendChild(style);