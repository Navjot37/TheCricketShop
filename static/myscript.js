function switchTab(event, myTab) {
    var i;
    var x = document.getElementsByClassName("thisTab");
    var tablinks = document.getElementsByClassName("tabLink");

    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(myTab).style.display = "block";
    event.currentTarget.className += " active";

}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.productId;

            fetch('/add_to_cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector('.cart').textContent = data.cart_count;
                } else {
                    alert("Could not add item to cart.");
                }
            });
        });
    });
});
