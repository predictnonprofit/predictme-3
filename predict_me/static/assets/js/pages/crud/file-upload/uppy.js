"use strict";

// Class definition
var KTUppy = function () {
	const Tus = Uppy.Tus;
	const ProgressBar = Uppy.ProgressBar;
	const StatusBar = Uppy.StatusBar;
	const FileInput = Uppy.FileInput;
	const Informer = Uppy.Informer;

	// to get uppy companions working, please refer to the official documentation here: https://uppy.io/docs/companion/
	const Dashboard = Uppy.Dashboard;
	const Dropbox = Uppy.Dropbox;
	const GoogleDrive = Uppy.GoogleDrive;
	const OneDrive = Uppy.OneDrive;
	const XHRUpload = Uppy.XHRUpload;
	const webSiteUrl = window.location.origin;
    const webSiteMemberUrl = window.location;


	// Private functions
	var initUppy1 = function(){
		var id = '#upload_donor_uppy';

		var options = {
			proudlyDisplayPoweredByUppy: false,
			target: id,
			inline: true,
			replaceTargetContent: true,
			showProgressDetails: true,
			note: 'Allowed filetypes, xlsx, xls, csv',
			height: 470,
			metaFields: [
				{ id: 'name', name: 'Name', placeholder: 'file name' },
				{ id: 'caption', name: 'Caption', placeholder: 'Donor data file' }
			],
			browserBackButtonClose: true
		}

		var uppyDashboard = Uppy.Core({ 
			autoProceed: true,
			// metadata: {
			// 	filename: file.name,
			// 	filetype: file.type
			// },
			retryDelays: [0, 3000, 5000, 10000, 20000],
			restrictions: {
				maxFileSize: 1000000, // 1mb
				// maxNumberOfFiles: 5,
				minNumberOfFiles: 1,
				// allowedFileTypes: ['image/jpg', 'image/jpeg', 'image/png'],
				
			},
			onError: function(error) {
				console.log("Failed because: " + error)
			},
			onProgress: function(bytesUploaded, bytesTotal) {
				var percentage = (bytesUploaded / bytesTotal * 100).toFixed(2)
				console.log(bytesUploaded, bytesTotal, percentage + "%")
			},
			onSuccess: function() {
				console.log("Download %s from %s", upload.file.name, upload.url)
			}
		});

		uppyDashboard.use(Dashboard, options);  
		uppyDashboard.use(Tus, {
			// endpoint: `${webSiteUrl}/dashboard/data/upload`, // use your tus endpoint here
			endpoint: `${webSiteUrl}/dashboard/data/upload/${fileName}`,
			// uploadUrl: `${webSiteUrl}/dashboard/data/upload`, // use your tus endpoint here
			resume: true,
			overridePatchMethod: "POST",
			autoRetry: true,
			retryDelays: [0, 1000, 3000, 5000],
			/* headers: {
				"X-CSRFToken": getCookie('csrftoken')
			}, */
			onBeforeRequest: function (req) {
				var xhr = req.getUnderlyingObject()
				// xhr.withCredentials = true;
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			},
			onError: function (err) {
				console.log("Error", err)
				console.log("Request", err.originalRequest)
				console.log("Response", err.originalResponse)
			},
			onProgress: function(bytesUploaded, bytesTotal) {
				var percentage = (bytesUploaded / bytesTotal * 100).toFixed(2)
				console.log(bytesUploaded, bytesTotal, percentage + "%")
			},
			onSuccess: function() {
				console.log("Download %s from %s", upload.file.name, upload.url)
			}
		});
	/* 	uppyDashboard.use(FileInput, {
			target: '.UppyForm',
			replaceTargetContent: true
		  }); */
		uppyDashboard.use(GoogleDrive, { target: Dashboard, companionUrl: 'https://companion.uppy.io' });
		uppyDashboard.use(Dropbox, { target: Dashboard, companionUrl: 'https://companion.uppy.io' });
		uppyDashboard.use(OneDrive, { target: Dashboard, companionUrl: 'https://companion.uppy.io' });
		/* uppyDashboard.use(XHRUpload, {
			bundle: true,
			endpoint: `${webSiteUrl}/dashboard/data/upload`,
			metaFields: ['something'],
			fieldName: 'donor_data_file',
			formData: true,
			headers: {
				"X-CSRFToken": getCookie('csrftoken'),
			},
			method: 'POST',
		  }); */
		  

		  
		  uppyDashboard.on('file-added', (file) => {
			alert(file);
		  });
		  
		  uppyDashboard.on('upload', (data) => {
			console.log("oon upload");
		  });
		  
		  uppyDashboard.on('complete', (result) => {
			alert(result);
		  });



	}



	return {
		// public functions
		init: function() {
			initUppy1();
			


			/* swal.fire({
				"title": "Notice", 
				"html": "Uppy demos uses <b>https://master.tus.io/files/</b> URL for resumable upload examples and your uploaded files will be temporarely stored in <b>tus.io</b> servers.", 
				"type": "info",
				"buttonsStyling": false,
				"confirmButtonClass": "btn btn-brand kt-btn kt-btn--wide",
				"confirmButtonText": "Ok, I understand",
				"onClose": function(e) {
					console.log('on close event fired!');
				}
			}); */
		}
	};
}();

KTUtil.ready(function() {	
	KTUppy.init();
});