import api from './api'
import { useAuthStore } from '@/store/authStore'

export const getGameTemplate = async (gameName) => {
    const response = await api.get(`/game/${gameName}/template`)
    if (response.status === 200) {
        const templateData = response.data
        const api_token = useAuthStore().api_token;
        const backend_url = api.defaults.baseURL;
        return templateData.replace(/%%API_TOKEN%%/g, api_token).replace(/%%API_BASE_URL%%/g, backend_url)
    }
    return null
}

export const getGameinfo = async (gameName) => {
    const response = await api.get(`/game/${gameName}/info`)
    return response.data
}
