$(document).ready(function(){
    var thumbs = $('.wall-thumb');
    thumbs.mouseenter(function(){
        $('.thumb-cover', this).fadeIn(100);
        $('.thumb-hover', this).fadeIn(100);
    });
    thumbs.mouseleave(function(){
        $('.thumb-cover', this).fadeOut(0);
        $('.thumb-hover', this).fadeOut(0);
    });
    Dropzone.autoDiscover = false;
    $(function() {
        // Now that the DOM is fully loaded, create the dropzone, and setup the
        // event listeners
        drop_settings = {
            maxFiles:1,
            uploadMultiple: false,
            url: "/drop/",
            acceptedFiles: "image/*",
            paramName: "file",
            dictDefaultMessage:"<i class=\"fa fa-cloud-upload fa-3x fa-green\"></i><br>클릭하거나 이미지를 끌어놓으세요",
            dictFallbackMessage:"실패"
        };
        var dz = new Dropzone(".dropzone",drop_settings);
        dz.on('success', function(file, response){
            console.log(response);
            window.location.href = window.location.protocol + '//' + window.location.host + '/i/' + response['id'] + '/';
        });
    });
    $('#upload-toggle').click(function(){
        $(this).toggleClass('active');
        $('.uploader').fadeToggle(100);
    });
});