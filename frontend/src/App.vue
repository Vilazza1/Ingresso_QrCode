<template>
  <div class="container">
    <h1>Cadastro de Ingresso</h1>

    <label>Nome do Titular</label>
    <input v-model="nomeTitular" type="text" />

    <label>Email</label>
    <input v-model="email" type="email" />

    <label>Telefone</label>
    <input v-model="telefone" type="tel" />

    <label>Documento (CPF/CNPJ)</label>
    <input v-model="documento" type="text" />

    <label>
      <input type="checkbox" v-model="temAcompanhante" />
      Possui acompanhante?
    </label>

    <div v-if="temAcompanhante">
      <label>Nome do Acompanhante</label>
      <input v-model="nomeAcompanhante" type="text" />
    </div>

    <button @click="enviarFormulario">Enviar</button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const nomeTitular = ref('')
const email = ref('')
const telefone = ref('')
const documento = ref('')
const temAcompanhante = ref(false)
const nomeAcompanhante = ref('')

const enviarFormulario = async () => {
  const payload = {
    nome_titular: nomeTitular.value,
    email: email.value,
    telefone: telefone.value,
    cnpj: documento.value,
    nome_acompanhante: temAcompanhante.value ? nomeAcompanhante.value : null
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      // tenta pegar a mensagem de erro do backend
      const errorData = await res.json()
      alert(`Erro: ${errorData.error || res.statusText}`)
      return
    }

    const data = await res.json()
    console.log('Resposta:', data)
    alert(data.msg)
  } catch (err) {
    console.error('Erro ao enviar:', err)
    alert('Erro ao enviar formulário.')
  }
}
</script>
