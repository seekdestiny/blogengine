$(document).ready(function () {
                $('.month').on('click', function () {
                     $(this).find('#caret-down').toggleClass('active');
                     $(this).find('#caret-up').toggleClass('active');
                });
            });
