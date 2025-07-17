$(document).ready(function () {
  // Add to cart
  $(".add-to-cart-btn").on("click", function () {
    let this_val = $(this);
    let index = this_val.attr("data-index");

    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_price = $(".current-product-price-" + index).text();
    let product_pid = $(".product-pid-" + index).val();
    let product_image = $(".product-image-" + index).val();

    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("ID:", product_id);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Index:", index);
    console.log("Current Element:", this_val);

    $.ajax({
      url: "/add-to-cart",
      data: {
        id: product_id,
        pid: product_pid,
        image: product_image,
        qty: quantity,
        title: product_title,
        price: product_price,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Adding Product to Cart...");
      },
      success: function (response) {
        this_val.html("Item added to cart");
        console.log("Added Product to Cart!");
        if ($(".cart-items-count").length > 0) {
          $(".cart-items-count").text(response.totalcartitems);
        } else {
          console.warn(".cart-items-count not found in DOM");
        }
      },
    });
  });

  // Delete product
  $(document).on("click", ".delete-product", function () {
    let this_val = $(this);
    let product_id = this_val.data("product");
    console.log("Product ID:", product_id);

    $.ajax({
      url: "/delete-from-cart",
      data: {
        id: product_id,
      },
      dataType: "json",
      beforeSend: function () {
        this_val.hide();
      },
      success: function (response) {
        $(".cart-items-count").text(response.totalcartitems);
        $("#cart-list").html(response.data);
      },
    });
  });

  // Load cart item count on page load
  $.ajax({
    url: "/cart-counter/",
    type: "GET",
    success: function (response) {
      if ($(".cart-items-count").length > 0) {
        $(".cart-items-count").text(response.totalcartitems);
        console.log(
          "Cart count refreshed on page load:",
          response.totalcartitems
        );
      } else {
        console.warn("cart-items-count not found when refreshing page");
      }
    },
  });
});
