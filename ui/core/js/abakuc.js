function get_regions(zone){
            $.ajax({
            type: "GET",
            url: '/users/0/;unimatrix?iana_root_zone=' + zone,
            dataType: 'json',
            success: function(data) {
                // add the returned HTML (the new select)
                var opts = '';
                $.each(data, function(i,item) {
                    opts += '<option>' + i + '</option>';
                });
                $("#regions").html('<select>' + opts + '</select>');

                }
            });
         
         } //end ajax call