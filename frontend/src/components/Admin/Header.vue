<template>
    <div class="w-full bg-transparent rounded-lg shadow-lg">
        <div class="flex items-center justify-between h-16 bg-gray-200 rounded-lg">
            <div class="p-4 cursor-pointer hover:bg-[#637575] rounded-lg" @click="clickHamburger">
                <i class="pi pi-bars text-gray-900"></i>
            </div>
            <div class="flex items-center flex-grow">
                <div class="py-2 mx-auto">
                    <span class="h-10 text-lg text-gray-900">{{ currentPage }}</span>
                </div>
            </div>
            <div class="p-4 cursor-pointer hover:bg-[#637575] rounded-lg">
                <i class="pi pi-question-circle text-gray-900 text-xl"></i>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        dataOpenSideBar: Boolean,
        clickHamburger: Function
    },
    computed: {
        currentPage() {
            return this.$route.name;
        }
    }
};
</script>

<style scoped>
/* Add scoped styles if necessary */
</style>
