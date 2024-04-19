import axios from 'axios';

class API {
    static endpoint = "http://127.0.0.1:8000";

    static async get(module: string, method: string) {
        const response = await axios.get(`${this.endpoint}/${module}/${method}`)
        return response.data;
    }

    static async post(module: string, method: string, data?: Object) {
        return await axios.post(`${this.endpoint}/${module}/${method}`, data);
    }

    static async getAllPlayers() {
        return await this.get('viewer', 'players');
    }
}

export default API