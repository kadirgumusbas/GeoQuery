import {defineStore} from 'pinia'
import {getRequest} from '@/services/apiService.js'

const storageKey = 'plans'
const requestKey = 'plans'

export const usePlanStore = defineStore('plan', {
    state: () => ({
        plans: [],
        loading: false,
        error: null,
    }),
    actions: {
        async initPlans() {
            this.loading = true
            try {
                const cached = localStorage.getItem(storageKey)
                if (cached) {
                    this.plans = JSON.parse(cached)
                } else {
                    const data = await getRequest(requestKey)
                    this.plans = data
                    localStorage.setItem(storageKey, JSON.stringify(data))
                }
            } catch (error) {
                console.log(this.plans)
                console.error(error)
            } finally {
                this.loading = false
            }

        },
    }
})
