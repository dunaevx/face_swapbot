/* script.js – чистый, с micro-interactions и a11y */
const tg = window.Telegram.WebApp;
tg.ready(); tg.expand();

const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

let selectedPhoto = null;
let selectedTemplate = null;

/* ---------- TAB SWITCH ---------- */
$$('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.tab;

        $$('.tab').forEach(t => t.classList.remove('active'));
        $(`#${target}`).classList.add('active');

        $$('.nav-btn').forEach(b => {
            b.classList.remove('active');
            b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
    });
});

/* ---------- PHOTO ---------- */
const photoInput = $('#photoInput');
const uploadLabel = $('#uploadLabel');
const preview = $('#preview');
const previewImg = $('#previewImg');
const clearBtn = $('#clearPreview');

photoInput.addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = ev => {
        selectedPhoto = ev.target.result.split(',')[1];
        previewImg.src = ev.target.result;
        preview.classList.remove('hidden');
        checkReady();
    };
    reader.readAsDataURL(file);
});

clearBtn.addEventListener('click', () => {
    photoInput.value = '';
    selectedPhoto = null;
    preview.classList.add('hidden');
    checkReady();
});

/* ---------- TEMPLATES ---------- */
$$('.template-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        $$('.template-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedTemplate = btn.dataset.template;
        checkReady();
    });
});

/* ---------- PROCESS ---------- */
const processBtn = $('#processBtn');
processBtn.addEventListener('click', () => {
    if (!selectedPhoto || !selectedTemplate) return;

    const payload = JSON.stringify({ photo: selectedPhoto, template_id: selectedTemplate });
    tg.sendData(payload);
    tg.showPopup({ message: 'Обработка запущена!' });
});

/* ---------- HELPERS ---------- */
function checkReady() {
    processBtn.disabled = !(selectedPhoto && selectedTemplate);
}

/* ---------- INITIAL STATE ---------- */
checkReady();