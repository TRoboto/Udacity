# Intel People Counter
Based on the Amplified starter kit, which uses...

- Webpack 2  
- React  
- Redux  
- Redux Thunk
- React Redux Router
- CSS Next
- Jest + Enzyme
- AirBnB ESLint  
  

### Requirements:
- Node 7.7.4+  
- Npm 4.1.2+  


### Setup
Update to latest packages:  
```
npm update --save --dev
```

Install dependencies:  
```
npm install
```


### Development
Start a local development server at http://localhost:3000/, build project, and watch files.
```
npm run dev
```
> You can access the dev build from any device on the network through your network IP address. If you don't know your IP, use this tool to find it https://www.npmjs.com/package/dev-ip  


### Folder Structure
__assets__   
> Contains all static assets. Create folders for fonts, images, and anything else.  

__components__  
> Small and highly reusable interface elements, these should rarely if ever be connected to redux.  

__constants__  
> Application constants for both js and css.  

__dux__  
> Short for redux in ducks style, there is generally one dux file per feature. Each dux file contains actions, action creators, and a reducer.  

__features__  
> Larger and more complex interface elements which generally do not get re-used. These will often be connected to redux via a Connected wrapper file.

__pages__  
> Entire application views which are rendered by the router.


### Styles
This repo does not include any CSS libraries.  
For a total CSS reset use https://www.npmjs.com/package/reset-css
```
npm install --save reset-css
```

Otherwise install normalize https://www.npmjs.com/package/normalize.css/
```
npm install --save normalize.css
```
