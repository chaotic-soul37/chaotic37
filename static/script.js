const socket = io.connect("http://localhost:5000");

socket.on("update_profiles", (profiles) => {
    const container = document.getElementById("profilesContainer");
    container.innerHTML = profiles.map(profile => `
        <div class="bg-gray-800 p-4 my-2 rounded">
            <h2 class="text-xl">${profile.name}</h2>
            <p>Status: <strong>${profile.status}</strong></p>
            <p>Used By: ${profile.user || '-'}</p>
            <p>Last Updated: ${profile.lastUpdated || '-'}</p>
            ${profile.status === "Available" 
                ? `<button onclick="useProfile(${profile.id})" class="bg-green-500 px-4 py-2 rounded mt-2">Use</button>` 
                : `<button onclick="releaseProfile(${profile.id})" class="bg-red-500 px-4 py-2 rounded mt-2">Free</button>`}
        </div>
    `).join("");
});

function useProfile(id) {
    const userName = prompt("Enter your name:");
    if (userName) {
        socket.emit("use_profile", { id, user: userName });
    }
}

function releaseProfile(id) {
    socket.emit("release_profile", { id });
}
