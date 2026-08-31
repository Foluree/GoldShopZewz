const world = document.getElementById('worldScene');
const form = document.getElementById('loginFrom');
const email = document.getElementById('email');
const password = document.getElementById('password');
const hint = document.getElementById('statusHint');

function updateScense() {
    world.classList.toggle('email',email.value.trim().length > 0);
    world.classList.toggle('password',password.value.trim().length > 0);

    if (!world.classList.contains('error')) {
        if (password.value.trim()) {
            hint.textContent = 'Пароль активировал свет и движение сцены.';
        } else if (email.value.trim()) {
            hint.textContent = 'Email начинает собирать мир вокруг формы.';
        } else {
            hint.textContent = 'Начни вводить email, чтобы «собрать» сцену.';
        }
    }
}

email.addEventListener('input', updateScense);
password.addEventListener('input', updateScense);

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const hasError = !email.value.trim() || !password.value.trim();

    world.classList.toggle('error', hasError);
    if (hasError) {
        hint.textContent = 'Ошибка: заполни оба поля. Мир временно «ломается». ';
        return;
    }

    hint.textContent = 'Демо: форма заполнена. Проверка на сервере пока отключена.';
    setTimeout(() => world.classList.remove('error'), 350);

    try {
        hint.textContent = 'Check database server...';
        const response = await fetch('/login/log', {
            method: 'POST',
            headers: {
"Content-Type":"application/json",
            },
            credentials: "include",
            body: JSON.stringify({
email_us: email.value.trim(),
passuse: password.value
            })
        });
        
        if (!response.ok) {
            world.classList.add('error');
            window.textContent = "Incorect email or password."
            return;
        } 

        hint.textContent = "Enterene complited. Transition the profile..."
        window.location.href = '/profile'
        
    } catch (error) {
        world.classList.add('error');
        hint.textContent = "Ошибка сети. По пробуйте еще раз.";
    } finally {
        setTimeout(() => world.classList.remove("error"), 450);
    }
});