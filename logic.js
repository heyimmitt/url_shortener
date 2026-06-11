document.addEventListener('DOMContentLoaded', () => {
	const form = document.querySelector('form');
	const longUrl = document.getElementById('long-url');
	const customName = document.getElementById('custom-name');
	const output = document.getElementById('shortened-url');

	function makeSlug() {
		return Math.random().toString(36).slice(2, 8);
	}

	form.addEventListener('submit', (e) => {
		e.preventDefault();
		const url = longUrl.value.trim();
		if (!url) {
			output.textContent = 'Please enter a URL.';
			return;
		}
		const slug = customName.value.trim() || makeSlug();
		const short = `${location.origin}/${slug}`;
		output.innerHTML = `<a href="${short}" target="_blank" rel="noopener noreferrer">${short}</a>`;
	});
});

