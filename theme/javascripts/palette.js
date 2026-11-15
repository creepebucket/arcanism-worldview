/* Material 默认只显示"下一个主题"的按钮, 这里把 4 个色块都放出来,
   并修正每个 label 指向的 radio —— 点哪个切到哪个。 */
(function () {
  function bind() {
    var form = document.querySelector(
      '.md-header__option[data-md-component="palette"]'
    );
    if (!form) return;

    var inputs = form.querySelectorAll("input.md-option");
    var labels = form.querySelectorAll("label.md-header__button");
    if (!inputs.length || inputs.length !== labels.length) return;

    Array.prototype.forEach.call(labels, function (label, i) {
      label.setAttribute("for", inputs[i].id);
      label.removeAttribute("hidden");
      label.hidden = false;
      label.style.display = "inline-flex";
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }

  // navigation.instant 会在站内跳转时重建页头
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(bind);
  }
})();
