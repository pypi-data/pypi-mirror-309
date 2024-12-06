HTMLElement.prototype.add_class = function(...classNames) {         // Adds class to current element
    this.classList.add(...classNames);
    return this
};

HTMLElement.prototype.remove_class = function(...classNames) {      // Removes class from current element
    this.classList.remove(...classNames);
    return this
};

HTMLElement.prototype.show = function() {
    this.style.display = '';                                        // Resets display to default
    return this
};

HTMLElement.prototype.hide = function() {                           // Hides element
    this.style.display = 'none';
    return this
};