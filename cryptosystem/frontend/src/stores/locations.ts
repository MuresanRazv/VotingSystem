import { readable } from "svelte/store";

type Location = {
    [key: string]: string[];
  };

const romaniaCities = readable<Location>({
    "Alba": ["Alba Iulia", "Aiud", "Sebeș"],
    "Arad": ["Arad", "Ineu", "Lipova"],
    "Argeș": ["Pitești", "Curtea de Argeș", "Costești"],
    "Bacău": ["Bacău", "Onești", "Moinești"],
    "Bihor": ["Oradea", "Salonta", "Beiuș"],
    "Bistrița-Năsăud": ["Bistrița", "Beclean", "Năsăud"],
    "Botoșani": ["Botoșani", "Dorohoi", "Darabani"],
    "Brăila": ["Brăila", "Ianca", "Făurei"],
    "Brașov": ["Brașov", "Făgăraș", "Săcele"],
    "București": ["București"],
    "Buzău": ["Buzău", "Râmnicu Sărat", "Nehoiu"],
    "Călărași": ["Călărași", "Oltenița", "Ștefan Vodă"],
    "Caraș-Severin": ["Reșița", "Caransebeș", "Oravița"],
    "Cluj": ["Cluj-Napoca", "Turda", "Dej"],
    "Constanța": ["Constanța", "Mangalia", "Medgidia"],
    "Covasna": ["Sfântu Gheorghe", "Târgu Secuiesc", "Covasna"],
    "Dâmbovița": ["Târgoviște", "Moreni", "Pucioasa"],
    "Dolj": ["Craiova", "Bailești", "Calafat"],
    "Galați": ["Galați", "Tecuci", "Târgu Bujor"],
    "Giurgiu": ["Giurgiu", "Bolintin-Vale", "Braniste"],
    "Gorj": ["Târgu Jiu", "Motru", "Rovinari"],
    "Harghita": ["Miercurea Ciuc", "Gheorgheni", "Odorheiu Secuiesc"],
    "Hunedoara": ["Deva", "Hunedoara", "Orăștie"],
    "Ialomița": ["Slobozia", "Fetești", "Țăndărei"],
    "Iași": ["Iași", "Pașcani", "Roman"],
    "Ilfov": ["Bragadiru", "Pantelimon", "Popești-Leordeni"],
    "Maramureș": ["Baia Mare", "Sighetu Marmației", "Borșa"],
    "Mehedinți": ["Drobeta-Turnu Severin", "Orșova", "Strehaia"],
    "Mureș": ["Târgu Mureș", "Sighișoara", "Reghin"],
    "Neamț": ["Piatra Neamț", "Roman", "Târgu Neamț"],
    "Olt": ["Slatina", "Caracal", "Corabia"],
    "Prahova": ["Ploiești", "Câmpina", "Sinaia"],
    "Satu Mare": ["Satu Mare", "Carei", "Negrești-Oaș"],
    "Sălaj": ["Zalău", "Șimleu Silvaniei", "Jibou"],
    "Sibiu": ["Sibiu", "Mediaș", "Cisnădie"],
    "Suceava": ["Suceava", "Rădăuți", "Fălticeni"],
    "Teleorman": ["Alexandria", "Roșiorii de Vede", "Turnu Măgurele"],
    "Timiș": ["Timișoara", "Lugoj", "Jimbolia"],
    "Tulcea": ["Tulcea", "Sulina", "Băneasa"],
    "Vâlcea": ["Râmnicu Vâlcea", "Drăgășani", "Băile Olănești"],
    "Vaslui": ["Vaslui", "Bârlad", "Huși"],
    "Vrancea": ["Focșani", "Adjud", "Mărășești"]
  });
  
  export default romaniaCities;