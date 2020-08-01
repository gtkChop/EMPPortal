document.addEventListener("DOMContentLoaded", function(){

    // this is to replace standard select form
    $('.select2-form').select2({
        width: 'resolve'
    });


    function readURL(input, target_id) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $(target_id).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]); // convert to base64 string
      }
    }

    $("#avatar-upload").change(function() {
        readURL(this, '.image-preview-avatar');
    });


    $(".tags-autocomplete").select2({
        tags: true,
        tokenSeparators: [','],
        createSearchChoice: function(term, data) {
            if ($(data).filter(function() {
              return this.text.localeCompare(term) === 0;
            }).length === 0) {
              return {
                id: term,
                text: term
              };
            }
        },
        minimumInputLength: 3,
        maximumSelectionLength: 10,
        createSearchChoice: function (term) {
            return {
                id: $.trim(term),
                text: $.trim(term) + ' (new tag)'
            };
        },
        multiple: true,
        ajax: {
            url: '/emapp/api/suggestion_employee_index',
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data: function(term, page) {
                var query = {
                    search: term,
                    search_field: $(this).attr("id")
               }
              return query;
            },
            processResults: function(data, params) {
                return {
                    results: data['result']
                };
            },
        }
    });


    $(".employee-autocomplete").select2({
        createSearchChoice: function(term, data) {
            if ($(data).filter(function() {
              return this.text.localeCompare(term) === 0;
            }).length === 0) {
              return {
                id: term,
                text: term
              };
            }
        },
        minimumInputLength: 2,
        maximumSelectionLength: 1,
        createSearchChoice: function (term) {
            return {
                id: $.trim(term),
                text: $.trim(term) + ' (new tag)'
            };
        },
        multiple: true,
        ajax: {
            url: '/emapp/api/suggestion_employee_index',
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data: function(term, page) {
                var query = {
                    search: term,
                    search_field: $(this).attr("id")
               }
              return query;
            },
            processResults: function(data, params) {
                return {
                    results: data['result']
                };
            },
        }
    });

});