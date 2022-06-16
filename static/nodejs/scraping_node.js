const puppeteer = require('puppeteer');


const { Client } = require('pg')
    const client = new Client({
        user: 'groupe7',
        host: 'localhost',
        database: 'flask_api',
        password: 'test_123',
        port: 5432,
    })
    client.connect(function(err) {
        if (err) throw err;
        console.log("Connected!");
    (async () => {
        const browser = await puppeteer.launch(
            {
                // la propriete headless a true va entraine l'ouverture du navigateur
                headless : true
            }
        );
        //   Creation d'une nouvelle onglet avec la methode newpage de browser
        const page = await browser.newPage();

    var l = 1
    // Navigation vers l'url souhaité
    for(var i = 1; i<=26; i++){
        await page.goto(`https://nova.sn/89-telephonie?page=${i}`);
        var price = await page.evaluate(()=>{
            let data = new Array()
            var tab =[]
            
            const div = document.querySelector('.center.col-12.col-md-8.col-lg-9')
            // console.log("gfgghghgghgg ",div)
            const element = div.querySelectorAll('.price.product-price')
            console.log(element)
            
            Array.from(element).forEach(elem => {
                console.log(elem.innerText)
                tab.push(elem.innerText)
            });

    
        return tab
        })

        // console.log(price);

        await page.waitForTimeout(5000)

        //   screenshot de la page puis stocker l'element sous le nom exemple.png
        //   await page.screenshot({ path: 'example.png' });
        
        // const price = await page.$$eval('.product-price)', allAs => allAs.innerText)
        const data = await page.$$eval('.second-block .product-name a', allAs => (allAs.map(a=>a.innerText)))
        // console.log(data)
        
        var j = 0
        
        
        for (elem of data){
            // console.log(elem)
            // var marque, modele, ROM, RAM, price;
            if (elem.startsWith('Apple iPhone')){
                
                var data_sp = elem.split(' ')
                if (data.length==9){
                    var rom = data_sp[3]
                    var ram = data_sp[5]
                }else{
                    var rom = data_sp[5]
                    var ram = data_sp[7]
                }

                var data_nova = {
                    'marque':'Iphone',
                    'modele':data_sp[0]+data_sp[1]+data_sp[2],
                    'ROM':rom,
                    'RAM':ram,
                    'price':price[j]
                }
                
                
                j+=1
            }else if(elem.startsWith('Samsung Galaxy')){
                
                var data_sp = elem.split(' ')
                if (elem.endsWith('Go', 'Go ')){
                    var ram = data_sp[data_sp.length]
                    var rom = data_sp[data_sp.length -2]
                }else{
                    var rom = data_sp[4]
                    var ram = data_sp[6]
                }
                var data_nova = {
                    'marque':'Samsung',
                    'modele':data_sp[0]+' '+data_sp[1]+' '+data_sp[2],
                    'ROM':rom,
                    'RAM':ram,
                    'price':price[j]
                }

                        
                    const insertTelText = 'INSERT INTO telephones(id_telephone, marque, modele, price, id_vendeur, id_car) VALUES ($1, $2, $3, $4, $5, $6)'
                    const insertCarText = 'INSERT INTO caracteristiques(id_car, memoire, ram) VALUES ($1, $2, $3)'
                    const insertTelValues = [l, data_nova['marque'], data_nova['modele'], data_nova['price'], 3, l]
                    const insertCarValues = [l, data_nova['ROM'], data_nova['RAM']]
                    console.log(insertTelValues)

                    client.query(insertCarText, insertCarValues, (err, res) => {
                    
                        client.query('COMMIT', err => {
                        if (err) {
                            console.error('Error committing transaction', err.stack)
                        }
                        
                        })
                    })
                    client.query(insertTelText, insertTelValues, (err, res) => {
                    
                        client.query('COMMIT', err => {
                        if (err) {
                            console.error('Error committing transaction', err.stack)
                        }
                        
                        })
                    })
                    l+=1

                // insert(l, data_nova['marque'], data_nova['modele'], data_nova['price'], 3, l)
                var mod = (data_nova.modele)
                j+=1
            } else{
                j+=1
            }
            console.log(mod)
        }
    }

    

    
    // client.connect(function(err) {
    //     if (err) throw err;
    //     console.log("Connected!");

    //     // function insert(id, marque, modele, price, id_vend, id_car){
    
            
    //             const insertTelText = 'INSERT INTO telephones(id_telephone, marque, modele, price, id_vendeur, id_car) VALUES ($1, $2, $3, $4, $5, $6)'
    //             const insertTelValues = [id, marque, modele, price, id_vend, id_car]
    //             console.log(insertTelValues)
    //             client.query(insertTelText, insertTelValues, (err, res) => {
                    
    //                 if ((err)) return
    //                 client.query('COMMIT', err => {
    //                 if (err) {
    //                     console.error('Error committing transaction', err.stack)
    //                 }
    //                 done()
    //                 })
    //             })
            
    //     // }///

    // });
    // Fermeture du navigateur
    await browser.close();

})();
})/////////

// function insert(id, marque, modele, price, id_vend, id_car){
    
//     const { Pool } = require('pg')
//     const pool = new Pool()
//     pool.connect((err, client, done) => {
    
//         const insertTelText = 'INSERT INTO telephones(id_telephone, marque, modele, price, id_vendeur, id_car) VALUES ($1, $2, $3, $4, $5, $6)'
//         const insertTelValues = [id, marque, modele, price, id_vend, id_car]
//         console.log(insertTelValues)
//         pool.query(insertTelText, insertTelValues, (err, res) => {
//             if ((err)) return
//             pool.query('COMMIT', err => {
//             if (err) {
//                 console.error('Error committing transaction', err.stack)
//             }
//             done()
//             })
//         })
     
//     })
// }