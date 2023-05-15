<script setup>
import PatientComponent from "@/components/PatientComponent.vue";
</script>

<template>
    <form type="multipart/form-data" class="form-container">
        <input type="text" name="patient_id" v-model="analysisForm.patient_id" class="input-element" placeholder="Идентификатор пациента">
        <input type="file" name="image" v-on:change="changeFile" class="input-element" alt="image-input">
        <button @click="onSubmit" class="input-element">Создать анализ</button>
    </form>
    <div>{{ msg }}</div>
    <div>
        <table>
            <tr>
                <th>№ п/п</th>
                <th>Результат анализа</th>
                <th>Дата</th>
                <th>Идентификатор пациента</th>
            </tr>
            <tr v-for="(patient, index) in patients" class="row" @click="getRow">
                <td>{{ index + 1 }}</td>
                <td>{{ patient.prediction }}</td>
                <td>{{ patient.date }}</td>
                <td>{{ patient.patient_id }}</td>
                <td style="display: none">{{ patient.image_bytes }}</td>
                <td style="display: none">{{ patient._id }}</td>
            </tr>
        </table>
        <dialog id="modal" @click="closeModal">
            <PatientComponent :diagnosis="selectedPatient[1]" :date="selectedPatient[2]"
                              :title="selectedPatient[3]" :img="selectedPatient[4]"
                              :id="selectedPatient[5]">
                <button @click="deletePatient" class="delete-button">Удалить</button>
            </PatientComponent>
        </dialog>
    </div>
</template>

<script>
import axios from "axios";
import { store } from '@/store'

export default
{
    data() {
        return {
            patients: [],
            selectedPatient: ['', '', '', '', ''],
            analysisForm: {
                patient_id: '',
                image: '',
            },
            analysisId: '',
            modal: '',
            msg: '',
        }
    },
    methods: {
        getAnalyzes() {
            axios.get("http://localhost:5000/analyzes", {headers: {Authorization: "Bearer " + localStorage.getItem('user-token')}})
                .then((res) => {
                    this.patients = res.data.data;
            })
        },
        deletePatient() {
            new Promise ((resolve, reject) => {
            axios.delete('http://localhost:5000/analyzes/' + this.selectedPatient[5], {headers: {Authorization: "Bearer " + localStorage.getItem('user-token')}})
                .then(resp => {
                    modal.close()
                    resolve(resp)
                })
                .catch((error) => {
                    this.msg = error.response.data.error;
                    reject(error)
                });
            }).then(() => {
                this.$router.push('/analyzes');
                this.getAnalyzes(); // TODO: WORST PRACTISES => REPLACE LATER
            })
        },
        getRow(event) {
            this.selectedPatient = [
                event.target.closest("tr").childNodes[0].innerText,
                event.target.closest("tr").childNodes[1].innerText,
                event.target.closest("tr").childNodes[2].innerText,
                event.target.closest("tr").childNodes[3].innerText,
                'data:image/png;base64, ' + event.target.closest("tr").childNodes[4].innerText,
                event.target.closest("tr").childNodes[5].innerText,
                ]
            modal.showModal()
        },
        closeModal(e) {
            const dialogDimensions = modal.getBoundingClientRect()
            if (
                e.clientX < dialogDimensions.left ||
                e.clientX > dialogDimensions.right ||
                e.clientY < dialogDimensions.top ||
                e.clientY > dialogDimensions.bottom
            ) {
                modal.close()
            }
        },
        changeFile(event){
            this.analysisForm.image = event.target.files[0];
        },
        createAnalysis(analysis) {
            new Promise ((resolve, reject) => {
                axios.post("http://localhost:5000/analyzes/predict", analysis, {headers: {Authorization: "Bearer " + localStorage.getItem('user-token'),}})
                    .then(resp => {
                        this.analysisId = resp.data.data._id
                        store.result = { // redundant if use modal
                            image_bytes: resp.data.data.image_bytes,
                            patient_id: resp.data.data.patient_id,
                            prediction: resp.data.data.prediction,
                            date: resp.data.data.date
                        }
                        resolve(resp)
                    })
                    .catch((error) => {
                        this.msg = error.response.data.error;
                        reject(error)
                    });
            }).then(() => {
                this.$router.push('/analyzes');
                this.getAnalyzes(); // TODO: WORST PRACTISES => REPLACE LATER
            })
        },
        initForm() {
            this.analysisForm.patient_id = '';
            this.analysisForm.image = '';
        },
        onSubmit(evt) {
            evt.preventDefault();

            let formData = new FormData()
            formData.append('patient_id', this.analysisForm.patient_id)
            formData.append('image', this.analysisForm.image)
            this.createAnalysis(formData);
            this.initForm();
        },
    },
    created() {
        this.getAnalyzes();

        this.modal = document.getElementById("modal")
    }
}
</script>

<style scoped>
    .form-container {
        display: grid;
        //justify-items: center;
        margin: 24px 0;
        width: 250px;
    }
    dialog {
        top: 50%;
        left: 50%;
        translate: -50% -50%;
        border-radius: 4px;
        border: 2px solid var(--vt-c-green);
    }
    .delete-button {
        color: white;
        background-color: var(--vt-c-text-red-light);
    }
    table {
        width: 100%;
        border-spacing: 0;
        border: 1px solid var(--vt-c-divider-dark-1);
    }
    td, th {
        border: 1px solid var(--vt-c-divider-dark-1);
    }
    th, td {
        padding: 5px 10px;
        border-top-width: 0;
        border-left-width: 0;
    }
    td {
        text-align: center;
    }
    th:last-child,
    td:last-child {
        border-right-width: 0;
    }
    tr:last-child td {
        border-bottom-width: 0;
    }
    .row:hover {
        background-color: var(--vt-c-green-light);
        cursor: pointer;
    }
    .input-element {
        margin: 12px 0;
    }
</style>