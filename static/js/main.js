// main.js — students will add JavaScript here as features are built

document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('how-it-works-btn');
    const modal = document.getElementById('video-modal');
    const backdrop = document.getElementById('video-modal-backdrop');
    const videoFrame = document.getElementById('video-iframe');
    const closeBtn = document.getElementById('video-modal-close');

    if (!openBtn || !modal || !videoFrame) {
        return;
    }

    function openModal() {
        const videoSrc = videoFrame.dataset.videoSrc || '';

        if (videoFrame.getAttribute('src') !== videoSrc) {
            videoFrame.setAttribute('src', videoSrc);
        }

        modal.hidden = false;
        openBtn.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.hidden = true;
        openBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';

        if (videoFrame.getAttribute('src')) {
            videoFrame.removeAttribute('src');
        }
    }

    openBtn.addEventListener('click', function(e) {
        e.preventDefault();
        openModal();
    });

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    if (backdrop) {
        backdrop.addEventListener('click', closeModal);
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !modal.hidden) {
            closeModal();
        }
    });
});
