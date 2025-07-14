$(function () {
  var min_val = 0;
  var max_val = 100;

  $("#slider-range").slider({
    range: true,
    min: min_val,
    max: max_val,
    values: [min_val, max_val],
    slide: function (event, ui) {
      $("#range").val("$" + ui.values[0] + " - $" + ui.values[1]);
      $("#max_price").val(ui.values[1]);
    },
  });

  $("#range").val(
    "$" +
      $("#slider-range").slider("values", 0) +
      " - $" +
      $("#slider-range").slider("values", 1)
  );
  $("#max_price").val($("#slider-range").slider("values", 1));

  $("#max_price").on("input", function () {
    var newMaxPrice = parseInt($(this).val());

    if (isNaN(newMaxPrice) || newMaxPrice < min_val) {
      newMaxPrice = min_val;
    } else if (newMaxPrice > max_val) {
      newMaxPrice = max_val;
    }

    var currentMin = $("#slider-range").slider("values", 0);

    if (newMaxPrice < currentMin) {
      currentMin = newMaxPrice;
    }

    $("#slider-range").slider("values", [currentMin, newMaxPrice]);

    $("#range").val(
      "$" +
        $("#slider-range").slider("values", 0) +
        " - $" +
        $("#slider-range").slider("values", 1)
    );
  });

  // Event listener for the Filter button
  $(".sidebar-widget .btn").on("click", function () {
    var maxPrice = parseInt($("#max_price").val());
    // Lấy URL từ thuộc tính data-
    var productListUrl = $(".shop-category-area").data("product-list-url"); // Hoặc bất kỳ phần tử nào bạn đã đặt data-
    window.location.href = productListUrl + "?max_price=" + maxPrice;
  });
});
