function DailyMotionXBlockStudio(runtime, element) {

    function saveHandler() {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {
            video_id: $(element).find('input[name=video_id]').val()
        };
        runtime.notify('save', {state: 'start'});
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            runtime.notify('save', {state: 'end'});
        });
    }

    function cancelHandler() {
        runtime.notify('cancel', {});
    }

    $(element).find('.save-button').bind('click', saveHandler);
    $(element).find('.cancel-button').bind('click', cancelHandler);
}
