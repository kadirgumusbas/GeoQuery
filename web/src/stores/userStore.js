import {defineStore} from 'pinia'

const storageKey = 'currentUser'

export const useUserStore = defineStore('user', {
    state: () => ({
        username: null,
        token: null,
    }),
    actions: {
        // Kullanıcıyı kaydet
        setUser(userData) {
            this.username = userData.username
            this.token = userData.token
            localStorage.setItem(storageKey, JSON.stringify(userData))
        },

        // LocalStorage'tan kullanıcıyı çek
        loadUserFromStorage() {
            const stored = localStorage.getItem(storageKey)
            if (stored) {
                const parse = JSON.parse(stored)
                this.username = parse.username
                this.token = parse.token
            }
        },

        // Çıkış
        logout() {
            this.username = null
            this.token = null
            localStorage.removeItem(storageKey)
        }
    }
})
