const email = document.getElementById('email');
const password = document.getElementById('password');
const passwordConfirm = document.getElementById('passwordConfirm');
const scene = document.getElementById('scene');
const dayNight = document.getElementById('dayNight');
const firmament = document.getElementById('firmament');
const land = document.getElementById('land');
const humans = document.getElementById('humans');
const status = document.getElementById('sceneStatus');
const help = document.getElementById('help');
const form = document.getElementById('registerForm');

function updateScene() {
    const hasEmail = email.value.trim().length > 3;
    const hasPassword = password.value.length >= 6;
    const passwordsMatch = password.value && password.value === passwordConfirm.value;

    scene.classList.remove('broken');
    help.classList.remove('error');

    dayNight.style.opacity = hasEmail ? '0.95' : '0.35';
    firmament.style.opacity = hasEmail ? "0.9":"0";
    firmament.style.transform = hasEmail ? 'translateY(0) scale(1)' : 'translateY(22px) scale(.97)';

    land.style.opacity = hasPassword ? '0.95' : '0';
    land.style.transform = hasPassword ? 'translateY(0) scale(1)':'translateY(28px) scale(.95)';

    humans.style.opacity = passwordsMatch ? '0.95':'0';
    humans.style.transform = passwordsMatch ? 'translateX(-50%) scale(1)':'translateX(-50%) scale(.82)';

    if (!hasEmail) {
        status.textContent = '1 day: light and dark.'
    } else if (!hasPassword) {
        status.textContent =  '2 day: Water separation, appers firmament.'
    } else if (!passwordsMatch && passwordConfirm.value.length > 0) {
        status.textContent = 'Error: structure collapse - password no coincide.';
        scene.classList.add('broken');
        help.textContent = 'Password no coincide.';
        help.classList.add('error');
    } else if (passwordsMatch) {
        status.textContent = '3 day: eart, life and humans appeared.';
        help.textContent = 'Form ready to seding.'
    } else {
        status.textContent = '3 day: forming eart.'
    }
}

[email,password,passwordConfirm].forEach(el => el.addEventListener('input',updateScene));

form.addEventListener('submit',(event) => {
    updateScene();
    const valid = email.checkValidity() && password.checkValidity() && password.value === passwordConfirm.value;
    if (!valid) {
        event.preventDefault();
        scene.classList.add('broken');
        status.textContent = "Error: data no full or no faithful.";
        help.textContent = "Check email and coincidence password."
        help.classList.add('error')
    }
});