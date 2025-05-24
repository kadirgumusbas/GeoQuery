import axios from 'axios'
import {useUserStore} from '@/stores/userStore'

const apiUrl = "http://127.0.0.1:8000"
const query = {
    plans: "membership-plans",
    users: "users",
    register: "register",
    login: "login",
    query: "query",
    monthly: "monthly-stats",
    pquery: "past-query",
    adminMonthly: "admin-monthly-stats",
    adminUser: "admin-user-stats",
    userGeo: "userGeo?username=",
    registerPlan: "register-plan",
    userPlan: "user-plan",
    isAdmin: "is-admin",
    adminUsers:"admin-monthly-users"
}

export async function getRequestUser(request, username) {
    const userStore = useUserStore()
    const token = userStore?.token

    const config = {}
    if (token) {
        config.headers = {
            Authorization: `Token ${token}`
        }
    }
    const url = `${apiUrl}/${query[request]}${username}`
    const response = await axios.get(url, config)
    return response.data
}

export async function getRequest(request) {
    const userStore = useUserStore();
    const token = userStore?.token;

    const config = {};
    if (token) {
        config.headers = {
            Authorization: `Token ${token}`
        };
    }

    const url = `${apiUrl}/${query[request]}/`
    const response = await axios.get(url, config);
    return response.data;
}

export async function postQuery(lat, lng) {
    const userStore = useUserStore();
    const token = userStore?.token;
    const config = {};

    if (token) {
        config.headers = {
            Authorization: `Token ${token}`
        };
    }
    const data = {
        lat: lat,
        lng: lng,
    };
    try {
        const response = await axios.post(`${apiUrl}/${query['query']}/`, data, config);
        return response.data;
    } catch (e) {
        const errorMsg =
            e.response?.data?.error ||
            e.response?.data?.detail || // yetkisiz erişim gibi genel hata
            'Sunucu hatası';
        throw new Error(errorMsg);
    }
}

export async function postUser(request, data) {
    const userStore = useUserStore();
    const token = userStore?.token;
    const config = {};

    if (token) {
        config.headers = {
            Authorization: `Token ${token}`
        };
    }
    try {
        const response = await axios.post(`${apiUrl}/${query[request]}/`, data, config);
        return response.data
    } catch (error) {
        const payload = error.response?.data || {non_field_errors: ['Sunucu hatası']}
        return Promise.reject(payload)
    }
}