const applyLazyLoading = () => {
    document.querySelectorAll(".kit-item-image").forEach((image) => {
        image.loading = "lazy";
    });
};

applyLazyLoading();
new MutationObserver(applyLazyLoading).observe(document.documentElement, {
    childList: true,
    subtree: true,
});
