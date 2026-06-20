document.addEventListener('DOMContentLoaded', () => {
	const form = document.querySelector('form');
	const longUrl = document.getElementById('long-url');
	const customName = document.getElementById('custom-name');
	const output = document.getElementById('shortened-url');

	// function makeSlug() {
	// 	return Math.random().toString(36).slice(2, 8);
	// }

	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		console.log('Form submitted, default prevented');

		const url = longUrl.value.trim();
		if (!url) {
			output.innerHTML = 'Please enter a URL.';
			return;
		}

		try {
			const response = await fetch("http://localhost:8000/shorten", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					long_url: url,
					custom_url: customName.value.trim() || null
				}),
			});

			if (!response.ok) {
				const errData = await response.json();
				output.innerHTML = errData.detail || "something went wrong";
				return;
			}

			const data = await response.json();
			const short_url = data.shortened_url;
			output.innerHTML = `<a href="${short_url}">${short_url}</a>`
		} catch (err) {
			output.innerHTML = "something went wrong"
		}
	});
});

