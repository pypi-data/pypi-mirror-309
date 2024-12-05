; !(function ($) {
    $.fn.django_ace_widget = function () {
        var self = $(this);
        // hide textarea
        var textarea = self.prev("textarea")
        textarea.hide();
        // build ace editor
        var editor_id = self.attr("id");
        var language = self.attr("language");
        var theme = self.attr("theme");
        var minLines = self.attr("minLines");
        var maxLines = self.attr("maxLines");
        var editor = ace.edit(editor_id, {
            mode: "ace/mode/" + language,
            theme: "ace/theme/" + theme,
            minLines: minLines,
            maxLines: maxLines
        });
        // init ace editor content
        editor.getSession().setValue(textarea.val());
        // copy ace editor content to textarea
        editor.getSession().on("change", function () {
            console.log(".");
            textarea.val(editor.getSession().getValue());
            console.log(textarea.val());
        });
    };

    $(document).ready(function () {
        $(".django_ace_widget_wrapper").each(function () {
            var self = $(this);
            if (!self.parents(".form-row").hasClass("empty-form")) {
                self.django_ace_widget();
            }
        });
    });

    $(document).on("formset:added", function (event) {
        var row = $(event.target);
        row.find(".django_ace_widget_wrapper").django_ace_widget();
    });
})(jQuery);