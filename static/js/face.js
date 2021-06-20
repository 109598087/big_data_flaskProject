function faceRegister() {
	$('#step3-nextBtn').attr('disabled', true);
	
	var faceImgBase64 = $('#faceImg').prop('src').replace(/^data:.*?;base64,/, "");
	var userModel = {
		'username': $('#username').val(),
		'picture': faceImgBase64
	};
	
	$.ajax({
		url: '/face',
		data: JSON.stringify(userModel),
		type: 'POST',
		dataType: 'json',
		success: function (response) {
			if(response.statusCode === 200) {
				console.log('upload image success');
				stepper.next();
			}
			
			else {
				console.log(response.body);
				alert(response.body);
				$('#step3-nextBtn').attr('disabled', false);
			}
		},
		error: function (error) {
			console.log(error);
			alert(error);
			$('#step3-nextBtn').attr('disabled', false);
		}
	});
}