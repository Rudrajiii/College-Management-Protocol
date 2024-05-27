fetch('/secret')
            .then(response => response.json())
            .then(data => {
                data.forEach(user => {
                    const data = [];
                    listItem = `ID: ${user.id}, Name: ${user.name}, Email: ${user.email}`;
                    data.push(listItem);
                });
                console.log(data);
            })
            .catch(error => console.error('Error fetching data:', error));
fetch('/logic')
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });

