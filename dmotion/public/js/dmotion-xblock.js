function InitializeVideoPlayer(element) {
    var dmotionXblock = $(element).find(".dmotion-xblock");
    var videoId = dmotionXblock.attr("data-video-id");
    return {
        player: DM.player(dmotionXblock[0], {
            video: videoId,
            width: "100%",
            height: 375
        }),
        videoId: videoId
    };
}

function InitializeDmotionXblockStudent(runtime, element) {
    var videoPlayer = InitializeVideoPlayer(element);
    var videoId = videoPlayer.videoId;
    var player = videoPlayer.player;

    function addEventListener(eventName) {
        player.addEventListener(eventName, onEvent(eventName));
    }

    // The following events are incompatible with the DailyMotion API:
    // https://developer.dailymotion.com/documentation#player-api-events
    // https://github.com/videojs/video.js/blob/stable/docs/api/vjs.Player.md#events
    // load_video : Supposed to be triggered on "loadstart". "Fired when the user agent begins looking for media data". Perhaps can we use the "progress" event?
    // video_hide_subtitle : no access to subtitles api
    // video_show_subtitle : no access to subtitles api
    // speed_change_video : no access to playback rate events
    addEventListener("apiready");
    addEventListener("play");
    addEventListener("pause");
    addEventListener("seeked");
    addEventListener("ended");

    function onEvent(eventName) {
        return function(data) {
            if (eventName == "apiready") {
                log('video_player_ready');
            }
            else if (eventName == "play") {
                log('play_video', {currentTime: currentTime()});
            }
            else if (eventName == "seeked") {
                log('seek_video', {new_time: currentTime()});
            }
            else if (eventName == "pause") {
                log('pause_video', {currentTime: currentTime()}); 
            }
            else if (eventName == "ended") {
                log('stop_video', {currentTime: currentTime()});
            }
        };
    }

    function currentTime() {
        return parseInt(player.currentTime);
    }

    function log(eventName, data) {
        if (typeof data === 'undefined') {
            data = {};
        }
        data.id = videoId;
        console.log(eventName, data);
        Logger.log(eventName, data);
    }
}
