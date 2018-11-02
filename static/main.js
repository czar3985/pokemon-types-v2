// Highlight the selected type from the sidebar
$(function () {
    var selected_type = $('.types-dropdown').val();
    $(`.type-text:contains("${selected_type}")`).addClass('type-highlight');
});

// Redirect to the page of the pokemon type selected from the dropdown
$('.types-dropdown').change(function () {
    window.location.href = '/pokemon/' + $(this).val();
});