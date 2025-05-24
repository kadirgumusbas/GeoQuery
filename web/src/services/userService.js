import {postUser} from "@/services/apiService.js";


export async function loginService(data) {
    const payload = {...data}
    const response = await postUser('login', payload)

    // Token'ı kaydet
    if (response.token) {
        localStorage.setItem('token', response.token)
    }
    return {
        username: response.username,
        token: response.token,
    }
}

export async function registerService(data) {
    if (data.password !== data.confirmPassword) {
        return alert('Passwords do not match')
    }
    const payload = {...data};
    return await postUser('register', payload)
}