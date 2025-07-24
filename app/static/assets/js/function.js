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

  // Update product
  $(document).on("click", ".update-product", function () {
    let this_val = $(this);
    let product_id = this_val.data("product");
    let product_quantity = $(".product-qty-" + product_id).val();

    console.log("Product ID:", product_id);
    console.log("Product QTY:", product_quantity);

    $.ajax({
      url: "/update-cart",
      data: {
        id: product_id,
        qty: product_quantity,
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

  // Making Default Address
  $(document).on("click", ".make-default-address", function () {
    let id = $(this).attr("data-address-id");
    let this_val = $(this);

    console.log("ID is:", id);
    console.log("Element is:", this_val);

    $.ajax({
      url: "/make-default-address",
      data: {
        id: id,
      },
      dataType: "json",
      success: function (response) {
        console.log("Address Made Default...");
        if (response.boolean == true) {
          $(".check").hide();
          $(".action_btn").show();

          $(".check" + id).show();
          $(".button" + id).hide();
        }
      },
    });
  });

  // Adding to wishlist
  $(document).on("click", ".add-to-wishlist", function () {
    let product_id = $(this).attr("data-product-item");
    let this_val = $(this);

    console.log("Product ID Is", product_id);

    $.ajax({
      url: "/add-to-wishlist",
      data: {
        id: product_id,
      },
      dataType: "json",
      beforeSend: function () {
        this_val.html("✔");
      },
      success: function (response) {
        if (response.bool === true) {
          console.log("Added to wishlist...|");
        }
      },
    });
  });

  // Remove from wishlist
  $(document).on("click", ".delete-wishlist-product", function () {
    let wishlist_id = $(this).attr("data-wishlist-product");
    let this_val = $(this);

    console.log("wishlist id is:", wishlist_id);

    $.ajax({
      url: "/remove-from-wishlist",
      data: {
        id: wishlist_id,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Deleting product from wishlist...");
      },
      success: function (response) {
        $("#wishlist-list").html(response.data);
      },
    });
  });
});
