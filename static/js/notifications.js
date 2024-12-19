

function toastSuccess(message, position, callback) {
    message = message || "Successful!";
    position = position || 'right';
    callback = callback || function() {};

    Toastify({
        text: message,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: position, // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
          background: "#28a745",
          color: "#fff"
        },
        callback: callback // Callback after click
    }).showToast();
}

function toastError(message, position, callback) {
    message = message || "Error!";
    position = position || 'right';
    callback = callback || function() {};

    Toastify({
        text: message,
        duration: 5000,
        newWindow: false,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: position, // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
          background: "#e63946",
          color: "#fff"
        },
        onClick: callback // Callback after click
    }).showToast();
}