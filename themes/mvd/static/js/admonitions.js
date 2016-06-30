/*
   Simple jQuery calls to replace RST admonitions with Bootstrap
   alerts.

   This is intended to work with the pelican-bootstrap3 Pelican theme,
   but may also work with others.

   This script is public domain.
*/

$('.note').addClass('alert').addClass('alert-info').removeClass('note');
$('.warning').addClass('alert').addClass('alert-warning').removeClass('warning');
