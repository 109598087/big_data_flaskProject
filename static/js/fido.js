let globalRegisteredCredentials = '';
let globalRegisteredCredentialsJSON = {};

createCredential = async () => {
	try {
		$('#fingerPrintBtn').attr('disabled', true);

		// build the credentials options requirements
		var credOptionsRequest = {
			attestation: 'none',
			username: $('#username').val(),
			name: $('#lineNickname').val(),
			authenticatorSelection: {
				authenticatorAttachment: 'platform',
				userVerification: 'preferred',
				requireResidentKey: false
			}
		};


		// generate credentials request to be sent to navigator.credentials.create
		var credOptions = await _fetch(fidoServerUrl + '/authn/createCredRequest', credOptionsRequest);
		var challenge = credOptions.challenge;

		credOptions.user.id = base64url.decode(credOptions.user.id);
		credOptions.challenge = base64url.decode(credOptions.challenge);

		// create credentials using available authenticator
		const cred = await navigator.credentials.create({
			publicKey: credOptions
		});

		// parse credentials response to extract id and public-key, this is the information needed to register the user in Cognito
		const credential = {};
		credential.id = cred.id;
		credential.rawId = base64url.encode(cred.rawId);
		credential.type = cred.type;
		credential.challenge = challenge;

		if (cred.response) {
			const clientDataJSON = base64url.encode(cred.response.clientDataJSON);
			const attestationObject = base64url.encode(cred.response.attestationObject);
			credential.response = {
				clientDataJSON,
				attestationObject
			};
		}

		credResponse = await _fetch(fidoServerUrl + '/authn/parseCredResponse', credential);

		globalRegisteredCredentialsJSON = { id: credResponse.credId, publicKey: credResponse.publicKey };
		globalRegisteredCredentials = JSON.stringify(globalRegisteredCredentialsJSON);
		var publicKeyCred = btoa(globalRegisteredCredentials);

		// credentials have been created, now bind the user's publicKey credential in Cognito
		var viewData = {
			'username': $('#username').val(),
			'custom:publicKeyCred': publicKeyCred
		};

		$.ajax({
			url: '/fido',
			data: JSON.stringify(viewData),
			type: 'POST',
			dataType: 'json',
			success: function (response) {
				if (response.statusCode === 200) {
					alert('綁定成功，請按「下一步」繼續');
					$('#step2-nextBtn').attr('disabled', false);
				}

				else {
					console.log(response.body);
					alert(response.body);
					$('#fingerPrintBtn').attr('disabled', false);
				}
			},
			error: function (error) {
				console.log(error);
				alert(error);
				$('#fingerPrintBtn').attr('disabled', false);
			}
		});


	} catch (e) {
		alert(e);
		console.error(e);
		$('#fingerPrintBtn').attr('disabled', false);
	}
};

_fetch = async (path, payload = '') => {
	const headers = { 'X-Requested-With': 'XMLHttpRequest' };
	if (payload && !(payload instanceof FormData)) {
		headers['Content-Type'] = 'application/json';
		payload = JSON.stringify(payload);
	}
	const res = await fetch(path, {
		method: 'POST',
		credentials: 'same-origin',
		headers: headers,
		body: payload
	});
	if (res.status === 200) {
		return res.json();
	}

	else {
		const result = await res.json();
		throw result.error;
		return res.json();
	}
};