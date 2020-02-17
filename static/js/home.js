/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/words',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(word) {
            let ajax_options = {
                type: 'POST',
                url: 'api/words',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(word)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(word) {
            let ajax_options = {
                type: 'PUT',
                url: `api/words/${word.word_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(word)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(word_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/words/${word_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $word_id = $('#word_id'),
        $word_name = $('#word_name');

    // return the API
    return {
        reset: function() {
            $word_id.val('');
            $word_name.val('');
        },
        update_editor: function(word) {
            $word_id.val(word.word_id);
            $word_name.val(word.word_name);
        },
        build_table: function(words) {
            let rows = ''

            // clear the table
            $('.words table > tbody').empty();

            // did we get a words array?
            if (words) {
                for (let i=0, l=words.length; i < l; i++) {
                    rows += `<tr data-word-id="${words[i].word_id}">
                        <td class="word_name">${words[i].word_name}</td>
                        <td>${words[i].distance}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $word_id = $('#word_id'),
        $word_name = $('#word_name');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(word_name) {
        return word_name !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let word_name = $word_name.val();

        e.preventDefault();

        if (validate(word_name)) {
            model.create({
                'word_name': word_name,
            })
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let word_id = $word_id.val(),
            word_name = $word_name.val();

        e.preventDefault();

        if (validate(word_name)) {
            model.update({
                word_id: word_id,
                word_name: word_name,
            })
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let word_id = $word_id.val();

        e.preventDefault();

        if (validate('placeholder', word_name)) {
            model.delete(word_id)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            word_id,
            word_name;

        word_id = $target
            .parent()
            .attr('data-word-id');

        word_name = $target
            .parent()
            .find('td.word_name')
            .text();

        view.update_editor({
            word_id: word_id,
            word_name: word_name,
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));

