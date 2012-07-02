$(document).ready ( function () {
    $(".editstring").blur ( function () {
        $.ajax ({
            url: "/admin/settextval",
            cache: false,
            type: "post",
            data: {file: $(this).attr ('name'), value: $(this).val()},
            dataType: "json",
            success: function () {},
            error: function () {},
        });
    });
});

