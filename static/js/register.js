function accountRegister() {
	if(!($('#username').val() && $('#password').val() && $('#email').val() && $('#lineNickname').val())) {
		alert('資料未填寫完整');
	}
	
	else {
		$('#step1-nextBtn').attr('disabled', true);
		
		var viewData = {
			'username': $('#username').val(),
			'password': $('#password').val(),
			'email': $('#email').val(),
			'name': $('#lineNickname').val(),
			'custom:role': $("input[type='radio'][name='role']:checked").val()
		};
		
		$.ajax({
			url: '/register/signUp',
			data: JSON.stringify(viewData),
			type: 'POST',
			dataType: 'json',
			success: function (response) {
				if(response.statusCode === 200) {
					var confirmationCode = prompt('請輸入email驗證碼:');
					viewData.confirmationCode = confirmationCode
					sendConfirmationCode(viewData);
				}
				
				else {
					console.log(response.body);
					alert(response.body);
					$('#step1-nextBtn').attr('disabled', false);
				}
			},
			error: function (error) {
				console.log(error);
				alert(error);
				$('#step1-nextBtn').attr('disabled', false);
			}
		});
	}
}

function sendConfirmationCode(viewData) {
	$.ajax({
		url: '/register/confirm',
		data: JSON.stringify(viewData),
		type: 'POST',
		dataType: 'json',
		success: function (response) {
			if(response.statusCode === 200) {
				console.log('Sign up success');
				stepper.next();
			}
			
			else {
				console.log(response.body);
				alert(response.body);
				$('#step1-nextBtn').attr('disabled', false);
			}
		},
		error: function (error) {
			console.log(error);
			alert(error);
			$('#step1-nextBtn').attr('disabled', false);
		}
	});
}