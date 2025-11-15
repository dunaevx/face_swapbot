const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Init data для auth
const user = tg.initDataUnsafe.user;

// Tabs
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(e.target.dataset.tab).classList.add('active');
        e.target.classList.add('active');
    });
});

// Upload photo
const photoInput = document.getElementById('photoInput');
const processBtn = document.getElementById('processBtn');
let selectedPhoto = null;
let selectedTemplate = null;

photoInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (ev) => {
            selectedPhoto = ev.target.result.split(',')[1];  // Base64
            processBtn.disabled = !selectedTemplate;
        };
        reader.readAsDataURL(file);
    }
});

// Select template
document.querySelectorAll('#templates button').forEach(btn => {
    btn.addEventListener('click', (e) => {
        selectedTemplate = e.target.dataset.template;
        processBtn.disabled = !selectedPhoto;
    });
});

// Process
processBtn.addEventListener('click', () => {
    if (selectedPhoto && selectedTemplate) {
        const data = {
            photo: selectedPhoto,
            template_id: selectedTemplate
        };
        tg.sendData(JSON.stringify(data));  // Отправка в бот
        tg.showAlert('Обработка запущена!');
    }
});

document.querySelectorAll('.template-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');

        selectedTemplate = e.target.dataset.template;
        processBtn.disabled = !selectedPhoto;
    });
});
