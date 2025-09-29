// DOM読み込み完了後に実行
document.addEventListener('DOMContentLoaded', function() {
    // ナビゲーションのアクティブ状態管理
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 外部リンクでない場合のみ処理
            if (!this.href.includes('http')) {
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // スムーススクロール
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 70; // ナビバーの高さを考慮
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // スクロール時のナビバー背景変更
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    });

    // アニメーション要素の表示制御
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-out forwards';
                entry.target.style.opacity = '1';
            }
        });
    }, observerOptions);

    // アニメーション対象の要素を監視
    const animateElements = document.querySelectorAll('.workflow-step, .feature-card, .tech-item, .status-card');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // プログレスバーのアニメーション
    const progressBars = document.querySelectorAll('.progress');
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 500);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });

    // カウンターアニメーション
    const counters = document.querySelectorAll('.stat-number');
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const finalValue = counter.textContent;
                const numericValue = parseInt(finalValue.replace(/\D/g, ''));

                if (!isNaN(numericValue)) {
                    animateCounter(counter, numericValue, finalValue);
                }
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });

    function animateCounter(element, finalValue, originalText) {
        let currentValue = 0;
        const increment = finalValue / 30;
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                element.textContent = originalText;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(currentValue) + (originalText.includes('+') ? '+' : '');
            }
        }, 50);
    }

    // モバイルメニューの制御（将来的な拡張用）
    function toggleMobileMenu() {
        const navMenu = document.querySelector('.nav-menu');
        navMenu.classList.toggle('active');
    }

    // ツールチップ機能
    const techItems = document.querySelectorAll('.tech-item');
    techItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // ワークフローステップのホバー効果
    const workflowSteps = document.querySelectorAll('.workflow-step');
    workflowSteps.forEach((step, index) => {
        step.addEventListener('mouseenter', function() {
            // 他のステップを少し薄く
            workflowSteps.forEach((otherStep, otherIndex) => {
                if (otherIndex !== index) {
                    otherStep.style.opacity = '0.7';
                }
            });
        });

        step.addEventListener('mouseleave', function() {
            // 全てのステップを元に戻す
            workflowSteps.forEach(otherStep => {
                otherStep.style.opacity = '1';
            });
        });
    });

    // パフォーマンス監視
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }, 0);
        });
    }
});