
/*del formulario de pregunta y respuestas*/
tinymce.init({
  selector: 'textarea#id_descripcion',
  height: 300,
  plugins: 'image media codesample imagetools link',
  toolbar: 'image media codesample',
  image_caption: true,
  media_live_embeds: true,
  imagetools_cors_hosts: ['tinymce.com', 'codepen.io'],
  language: 'es',
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//cdnjs.cloudflare.com/ajax/libs/prism/0.0.1/prism.css',
    '//www.tinymce.com/css/codepen.min.css'    
  ]
  
});

/* del formulario de post_form*/
tinymce.init({
  selector: '#id_text',
  height: 300,
  plugins: 'image media codesample imagetools link',
  toolbar: 'image media codesample',
  image_caption: true,
  media_live_embeds: true,
  imagetools_cors_hosts: ['tinymce.com', 'codepen.io'],
  language: 'es',
  content_css: [
    '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    '//cdnjs.cloudflare.com/ajax/libs/prism/0.0.1/prism.css',
    '//www.tinymce.com/css/codepen.min.css'    
  ]
  
});


/* del formulario de detalle de preguntas*/
tinymce.init({
  selector: 'textarea#descripcionPregunta',
  height: 350,
  plugins: 'image media codesample imagetools code',
  theme: 'modern',
  toolbar: false,
  menubar: false,
  /*inline: true,*/
  readonly: true,
  /*statusbar: false*/
  
  
});
/*del formulario de detalle de pregunta la opcion para respuesta*/
tinymce.init({
  selector: 'textarea#descripcionRespuesta',
  height: 80,
  plugins: 'image media codesample imagetools code',
  theme: 'modern',
  toolbar: false,
  menubar: false,
  /*inline: true,*/
  readonly: true,
  /*statusbar: false*/
  
  
});

tinymce.init({
  selector: 'textarea#preguntasFrecuentes',
  height: 100,
  plugins: 'image media codesample imagetools code autoresize',
  theme: 'modern',
  toolbar: false,
  menubar: false,
  readonly: true,
  statusbar: false,
  autoresize_overflow_padding: 0
  
  
});

/*del form de publicacion de post*/
tinymce.init({
  selector: 'textarea#descripcionBlog',
  height: 100,
  plugins: 'image media codesample imagetools code',
  theme: 'modern',
  toolbar: false,
  menubar: false,
  /*inline: true,*/
  readonly: true,
  /*statusbar: false*/
  
  
});