setTimeout(() => {
  const nodes = document.querySelectorAll('*').length;
  if (nodes < 200) {
    const banner = document.createElement('div');
    banner.innerHTML = 'WebEcho-Lite: Ollama-Generated Page (DOM sparsity detected)';
    banner.style.cssText = 'background:#d4edda;color:#155724;padding:10px;position:fixed;top:0;left:0;width:100%;z-index:9999;font-weight:bold;text-align:center;';
    document.body.prepend(banner);
  }
}, 1000);
