var task_id = null;
var task_status = null;

const statuses = {
    RESPONSED: "Получен ответ",
    QUEUED: "Запрос в очереди на обработку",
    STARTED: "Обрабатывается"
}

const make_get = () => {
    $.ajax({
        url: `/api/v1/tasks/${task_id}`,
        contentType: 'application/json; charset=utf-8',
        type: 'GET',
        async: true,
        success: on_success
    });
}

const on_success = (data) => {
    $('#result_card').show();
    $('#task_id_val').text(data.id);
    $('#status_val').text(statuses[data.status]);
    let msg = "Обработано";
    if(data.status === 'RESPONSED'){
        M.toast({html: msg, displayLength: 2000})
        $('#card_title').show();
        $('#response').show();
        $('#response').text(data.result);
    } else {
        msg = "Ваш запрос обрабатывается"
        if (data.status === 'QUEUED'){
            msg = "Ваш запрос добавлен в обработку"
        }
        if (data.status != task_status){
            M.toast({html: msg, displayLength: 2000})
            task_status = data.status;
        }
        task_id = data.id;
        setTimeout(make_get, 1000);
    }
}


var element = document.getElementById("send_btn");
element.onclick = (event) => {
    task_id = null;
    task_status = null;
    var question = $('#question').val();
    $('#card_title').hide();
    $('#response').hide();
    $.ajax({
        url: '/api/v1/inference',
        type: 'POST',
        data: JSON.stringify({'question': question}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
        success: on_success
    });
}